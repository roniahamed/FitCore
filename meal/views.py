from rest_framework import viewsets, status, filters 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone 

from .models import Food, Meal, MealPlan, ScheduledMeal
from .serializers import FoodSerializer, MealSerializer, MealPlanSerializer
from .permission import IsOwner, IsOwnerOrAdmin, IsFoodOwnerOrPublic
from django.db import transaction


class FoodViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Food items.
    Functionality:
    - List public foods and user's private foods.
    - Retrieve specific food.
    - Create private food (or public if admin).
    - Update/Delete user's private food (or any if admin).
    - Search foods database.
    """
    serializer_class = FoodSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['name', 'description', 'food_category__iexact']
    ordering_fields = ['name', 'calories', 'protein', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Food.objects.filter(Q(is_public=True)|Q(user_added=user)).distinct()
        return Food.objects.filter(is_public=True)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsFoodOwnerOrPublic()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else: 
            return super().get_permissions()
        
    def perform_create(self, serializer):
        # Serializer's create method handles assigning user_added based on context and is_public flag
        serializer.save() # Pass request to serializer context if needed for user_added logic
                          # My serializer already accesses self.context.get('request')



class MealViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user's Meals.
    Meals are private to the user.
    """
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Ensures only owner can access/modify

    def get_queryset(self):
         # Users can only see and manage their own meals
        return Meal.objects.filter(user = self.request.user).prefetch_related('mealitem_set__food')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user's Meal Plans.
    Provides functionalities:
    - Create a manual meal plan (POST /)
    - Update a meal plan (PUT/PATCH /{id}/)
    - Cancel a user’s meal plan (PATCH /{id}/cancel/)
    - Get all meal plans of a specific user (GET /)
    - Get a specific meal plan by ID (GET /{id}/)
    - Delete a meal plan (DELETE /{id}/)
    - Get available meal plan templates (GET /templates/)
    - Copy an existing meal plan (POST /{id}/copy/)
    """

    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if self.action == 'list_templates':
            # For the custom action
            # Templates are MealPlan instances marked as 'is_template'
            # Or define templates differently, e.g., user=None or owned by admin
            # Assuming 'is_template' field exists on MealPlan model:
            return MealPlan.objects.filter(is_template=True, is_active=True).prefetch_related('scheduledmeal_set__meal__mealitem_set__food')
        
        # For standard list, retrieve, update, delete -> user's own meal plans
        return MealPlan.objects.filter(user=user).prefetch_related('scheduledmeal_set__meal__mealitem_set__food')
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'cancel_user_meal_plan']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'list_templates':
            return [IsAuthenticatedOrReadOnly()]
        elif self.action == 'copy_meal_plan': # Permission for the copy action
            return [IsAuthenticated()] # Any authenticated user can attempt to copy a plan they can view
        return super().get_permissions()
    
    def perform_create(self, serializer):
        user = self.request.user

        is_template_request = serializer.validated_data.get('is_template', 'false')

        if is_template_request:
            if not( user.is_staff or user.is_superuser):
                raise PermissionDenied('You do not have permission to create a template.')
            serializer.save(user=user, is_template = True)
        else:
            serializer.save(user=user, is_template=False)
    
    @action(detail=True, methods=['patch'], url_path='cancel', permission_classes=[IsAuthenticated, IsOwner])
    def cancel_user_meal_plan(self, request, pk=None):
        """
        Cancel a user’s meal plan (sets is_active to False).
        """
        meal_plan = self.get_object()  # get_object already enforces IsOwner permission from get_permissions
        meal_plan.is_active = False 
        meal_plan.save()
        serializer = self.get_serializer(meal_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='templates', permission_classes=[IsAuthenticatedOrReadOnly])
    def list_templates(self, request):
        """
        Get available meal plan templates.
        (Requires 'is_template' field on MealPlan model or adjust filter in get_queryset)
        """

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='copy')
    def copy_meal_plan(self, request, pk=None):
        """
        Copies an existing meal plan for the current authenticated user.
        The original plan can be a template or another user's plan (if visible).
        The new plan will be owned by the request.user.
        """

        original_plan = self.get_object()
        user = request.user

        if original_plan.user == user and not original_plan.is_template:
            return Response({'detail': 'You already own this meal plan.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic(): # Ensure atomicity: all or nothing
                new_plan = MealPlan.objects.create(
                    user=user,
                    name=f"{original_plan.name} (Copy)",
                    description=original_plan.description,
                    duration_days=original_plan.duration_days,
                    is_active=True,
                    is_template=False,
                    start_date=None,
                    goal=original_plan.goal,
                    target_daily_calories=original_plan.target_daily_calories,
                )

                original_scheduled_meals = original_plan.scheduledmeal_set.all()
                new_scheduled_meals_to_create = []
                for original_sm in original_scheduled_meals:
                    new_scheduled_meals_to_create.append(
                        ScheduledMeal(
                            meal_plan=new_plan,
                            meal=original_sm.meal,  # Reference the same Meal object
                            day_of_plan=original_sm.day_of_plan
                        )
                    )
                if new_scheduled_meals_to_create:
                    ScheduledMeal.objects.bulk_create(new_scheduled_meals_to_create)
                
                serializer = self.get_serializer(new_plan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            

        except Exception as e:
            print(f"Error copying meal plan: {e}") # Basic logging
            return Response(
                {"detail": "An error occurred while copying the meal plan."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        