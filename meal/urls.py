from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealViewSet, FoodViewSet, MealPlanViewSet

router = DefaultRouter
router.register(r'food', FoodViewSet, basename='food' )
router.register(r'meals', MealPlanViewSet, basename='meal')
router.register(r'meal-plans', MealPlanViewSet, basename='mealplan' )


urlpatterns = [
    path('', include(router.urls)), 
]