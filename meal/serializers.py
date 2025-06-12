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

class MealSerializer(serializers.ModelSerializer):
    user_detail = CustomSerializer(source='user', read_only = True)
    meal_items = MealItemSerializer(many=True, source='mealitem_set')

    meal_items_payload = MealItemSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Meal 
        fields = ['id', 'user', 'user_detail', 'name', 'meal_time_category', 'description', 'is_template',
            'meal_items', # For reading existing items
            'meal_items_payload', # For creating/updating items
            'total_calories', 'total_protein', 'total_carbohydrates', 'total_fat',
            'created_at', 'updated_at']
        read_only_fields = [
            'id', 'user', 'user_detail', 'created_at', 'updated_at', 'meal_items',
            'total_calories', 'total_protein', 'total_carbohydrates', 'total_fat'
        ]
    def _handle_meal_items(self, meal_instance, meal_items_payload):
        if meal_items_payload is None:
            return 
        existing_items = {item.id: item for item in meal_instance.mealitem_set.all()}
        incoming_ids = set()
        for item_data in meal_items_payload:
            item_id = item_data.get('id', None)
            if item_id and item_id in existing_items:
                item = existing_items[item_id]
                item.food_id = item_data['food']
                item.number_of_servings = item_data['number_of_servings']
                item.save()
                incoming_ids.add(item_id)
            else:
                MealItem.objects.create(meal=meal_instance, food_id= item_data['food'], number_of_servings=item_data['number_of_servings'])
        for item_id in existing_items:
            if item_id not in incoming_ids:
                existing_items[item_id].delete()
        
    def create(self, validated_data):
        meal_items_payload = validated_data.pop('meal_items_payload', [])
        meal = Meal.objects.create(**validated_data)
        self._handle_meal_items(meal, meal_items_payload)
        return meal 
    
    def update(self, instance, validated_data):
        meal_items_payload = validated_data.pop('meal_items_payload', None)

        instance = super().update(instance, validated_data)

        if meal_items_payload is not None:
            self._handle_meal_items(instance, meal_items_payload)
        return instance