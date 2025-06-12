from rest_framework import serializers
from .models import Food, Meal, MealItem, MealPlan, ScheduledMeal
from users.serializers import CustomSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class FoodSerializer(serializers.ModelSerializer):
    user_added_detail = CustomSerializer(source='user_added', read_only=True)
    user_added = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null = True)

    class Meta:
        model = Food
        fields = [
            'id', 'name', 'description', 'serving_quantity', 'serving_unit', 'calories','protein', 'carbohydrates', 'fat', 'fiber', 'sugar', 'sodium', 'food_category','user_added', 'user_added_detail', # Use user_added for write, user_added_detail for read
            'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_added_detail', 'created_at', 'updated_at']
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        if user and user.is_authenticated:
            validated_data['user_added'] = request.user 
        else:
            validated_data['user_added'] = None
        return super().create(validated_data)

class MealItemSerializer(serializers.ModelSerializer):
    food_detail = FoodSerializer(source='food', read_only=True)
    food = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), write_only=True)

    class Meta:
        model = MealItem
        fields = [ 'id', 'meal', 'food', 'food_detail', 'number_of_servings',
            'calculated_calories', 'calculated_protein', 'calculated_carbohydrates', 'calculated_fat']
        read_only_fields = ['id', 'meal', 'food_detail', 'calculated_calories', 'calculated_protein', 'calculated_carbohydrates', 'calculated_fat']    
