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



