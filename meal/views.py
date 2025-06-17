from rest_framework import viewsets, status, filters 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q

from .models import Food, Meal, MealPlan
from .serializers import FoodSerializer, MealSerializer, MealPlanSerializer
from .permission import IsOwner, IsOwnerOrAdmin, IsFoodOwnerOrPublic


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

    search_fields = ['name', 'brand_name', 'description', 'food_category_iexact']
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
            return super().get_permission()
        
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
        return MealPlan.objects.filter(user=user).prefetch_related('scheduledmeal_set__meal__mealitem_set__food')
    
