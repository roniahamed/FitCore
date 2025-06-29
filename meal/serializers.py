from rest_framework import serializers
from .models import Food, Meal, MealItem, MealPlan, ScheduledMeal
from users.serializers import CustomSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class FoodSerializer(serializers.ModelSerializer):
    user_added_detail = CustomSerializer(source='user_added', read_only=True)

    class Meta:
        model = Food
        fields = [
            'id', 'name', 'description', 'serving_quantity', 'serving_unit', 'calories','protein', 'carbohydrates', 'fat', 'fiber', 'sugar', 'sodium', 'food_category','user_added_detail', # Use user_added for write, user_added_detail for read
            'is_public',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_added_detail', 'created_at', 'updated_at', 'user_added']
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
    meal_items = MealItemSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Meal 
        fields = ['id', 'user', 'user_detail', 'name', 'meal_time_category', 'description', 'is_template',
            'meal_items', 
            'total_calories', 'total_protein', 'total_carbohydrates', 'total_fat',
            'created_at', 'updated_at']
        read_only_fields = [
            'id', 'user', 'user_detail', 'created_at', 'updated_at',
            'total_calories', 'total_protein', 'total_carbohydrates', 'total_fat'
        ]
    def _handle_meal_items(self, meal_instance, meal_items_payload):
        if meal_items_payload is not None:
            existing_items = {item.id: item for item in meal_instance.mealitem_set.all()}
            # print(meal_items_payload)
            incoming_ids = set()
            for item_data in meal_items_payload:
                item_id = item_data.get('id', None)
                food_instance = item_data.get('food')
                number_of_servings = item_data.get('number_of_servings')
                if item_id is not None and item_id in existing_items:
                    meal_item = existing_items[item_id]
                    meal_item.food = food_instance
                    meal_item.number_of_servings = number_of_servings
                    meal_item.save()
                    incoming_ids.add(item_id)
                elif food_instance and number_of_servings is not None:
                    # create new Item
                    new_item = MealItem.objects.create(meal=meal_instance, food= food_instance, number_of_servings=number_of_servings)
                    incoming_ids.add(new_item.id)
            for item_id in existing_items:
                if item_id not in incoming_ids:
                    existing_items[item_id].delete()
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['meal_items'] = MealItemSerializer(instance.mealitem_set.all(), many=True).data 
        return representation
        
    def create(self, validated_data):
        meal_items_payload = validated_data.pop('meal_items', [])
        meal = Meal.objects.create(**validated_data)
        self._handle_meal_items(meal, meal_items_payload)
        return meal 
    
    def update(self, instance, validated_data):
        meal_items_payload = validated_data.pop('meal_items', None)

        instance = super().update(instance, validated_data)

        if meal_items_payload is not None:
            self._handle_meal_items(instance, meal_items_payload)
        return instance

class ScheduledMealSerializer(serializers.ModelSerializer):
    meal_detail = MealSerializer(source='meal', read_only=True)    
    meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), write_only=True)

    class Meta:
        model = ScheduledMeal
        fields = ['id', 'meal_plan', 'meal', 'meal_detail', 'day_of_plan']

        read_only_fields = ['id', 'meal_plan', 'meal_detail']


class MealPlanSerializer(serializers.ModelSerializer):
    user_detail = CustomSerializer(source='user', read_only=True)
    scheduled_meals = ScheduledMealSerializer(many=True, read_only=True, required=False)
    is_template = serializers.BooleanField(required=False, default=False)
    scheduled_meals_payload = ScheduledMealSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = MealPlan 
        fields = [
            'id', 'user', 'user_detail', 'name', 'description', 'goal', 'duration_days', 'start_date',
            'target_daily_calories', 'is_active',
            'is_template', 
            'scheduled_meals', # For reading existing items
            'scheduled_meals_payload', # For creating/updating items
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'user_detail', 'scheduled_meals', 'created_at', 'updated_at']

    def _handle_scheduled_meals(self, meal_plan_instance, scheduled_meals_payload):
        if scheduled_meals_payload is not None:
            existing_meals = {sm.id:sm for sm in meal_plan_instance.scheduledmeal_set.all()}
            incoming_item_ids = set()

            for item_data in scheduled_meals_payload:
                item_id = item_data.get('id', None)
                if item_id and item_id in existing_meals:
                    scheduled_meal = existing_meals[item_id]
                    scheduled_meal.day_of_plan = item_data.get('day_of_plan', scheduled_meal.day_of_plan)
                    scheduled_meal.save()
                    incoming_item_ids.add(item_id)
                else:
                    scheduled_meal = ScheduledMeal.objects.create(meal_plan= meal_plan_instance, meal=item_data['meal'], day_of_plan=item_data['day_of_plan'] )
                    incoming_item_ids.add(scheduled_meal.id)
            
            for meal_id, meal_instance in existing_meals.items():
                if meal_id not in incoming_item_ids:
                    meal_instance.delete()

    def create(self, validated_data):
        scheduled_meals_payload = validated_data.pop('scheduled_meals_payload', [])

        meal_plan = MealPlan.objects.create(**validated_data)

        self._handle_scheduled_meals(meal_plan, scheduled_meals_payload)

        return meal_plan
    def update(self, instance, validated_data):

        scheduled_meals_payload = validated_data.pop('scheduled_meals_payload', None)

        instance = super().update(instance, validated_data)

        if scheduled_meals_payload is not None:
            self._handle_scheduled_meals(instance, scheduled_meals_payload)
        return instance
