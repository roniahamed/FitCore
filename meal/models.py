from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


# Helper Constants (Choices)
class FoodCategory(models.TextChoices):
    FRUIT = 'FR', 'Fruit'
    VEGETABLE = 'VG', 'Vegetable'
    GRAIN = 'GR', 'Grain'
    PROTEIN = 'PR', 'Protein Food'
    DAIRY = 'DR', 'Dairy'
    FAT_OIL = 'FO', 'Fat & Oil'
    BEVERAGE = 'BV', 'Beverage'
    OTHER = 'OT', 'Other'

class MealTimeCategory(models.TextChoices):
    BREAKFAST = 'BF', 'Breakfast'
    LUNCH = 'LN', 'Lunch'
    DINNER = 'DN', 'Dinner'
    SNACK = 'SN', 'Snack'
    PRE_WORKOUT = 'PRE', 'Pre-workout'
    POST_WORKOUT = 'POST', 'Post-workout'

class MealPlanGoal(models.TextChoices):
    WEIGHT_LOSS = 'WL', 'Weight Loss'
    WEIGHT_GAIN = 'WG', 'Weight Gain'
    MAINTENANCE = 'MN', 'Maintenance'
    MUSCLE_GAIN = 'MG', 'Muscle Gain'
    GENERAL_HEALTH = 'GH', 'General Health'


class Food(models.Model):
    name = models.CharField(max_length=200, verbose_name="Food Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    # Serving information
    # serving_quantity: e.g., 100 (for grams), 1 (for cup/piece)
    # serving_unit: e.g., "g", "cup", "piece", "slice"
    serving_quantity = models.FloatField(default=1.0, validators=[MinValueValidator(0.01)], verbose_name="Serving Quantity (Numeric)")
    serving_unit = models.CharField(max_length=50, default="g", verbose_name="Serving Unit") # e.g., g, piece, cup, tbsp

     # Nutritional information (per `serving_quantity` `serving_unit`)
    calories = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Calories")
    protein = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Protein (g)")
    carbohydrates = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Carbohydrates (g)")
    fat = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Fat (g)")
    fiber = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Fiber (g)")
    sugar = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Sugar (g)")
    sodium = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Sodium (mg)")
    food_category = models.CharField(max_length=2, choices=FoodCategory.choices, default=FoodCategory.OTHER, verbose_name='Food Category')
     # If the user added this custom food
    user_added = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_foods', verbose_name="Added by User")
    is_public = models.BooleanField(default=True, verbose_name="Publicly Available") # True if admin adds a general food item
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.serving_quantity} {self.serving_unit})"

    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"
        ordering = ['name']


class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meals', verbose_name="User")
    name = models.CharField(max_length=100, verbose_name="Meal Name") # e.g., Breakfast, Lunch
    meal_time_category = models.CharField(
        max_length=4, 
        choices=MealTimeCategory.choices,
        default=MealTimeCategory.SNACK,
        verbose_name="Meal Time Category"
    )
    
    description = models.TextField(blank=True, null=True, verbose_name="Description")
     # The `foods` field will be a ManyToManyField via `MealItem`
    foods = models.ManyToManyField(Food, through='MealItem', related_name='meals_containing', verbose_name="Foods")
    
    is_template = models.BooleanField(default=False, verbose_name="Is Template Meal?") # Reusable template

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.get_meal_time_category_display()})"
    
    # Properties for total nutrition calculation
    @property
    def total_calories(self):
        return sum(item.calculated_calories for item in self.mealitem_set.all() if item.calculated_calories is not None)
    @property
    def total_protein(self):
        return sum(item.calculated_protein for item in self.mealitem_set.all() if item.calculated_protein is not None)

    @property
    def total_carbohydrates(self):
        return sum(item.calculated_carbohydrates for item in self.mealitem_set.all() if item.calculated_carbohydrates is not None)

    @property
    def total_fat(self):
        return sum(item.calculated_fat for item in self.mealitem_set.all() if item.calculated_fat is not None)

    @property
    def total_fiber(self):
        return sum(item.calculated_fiber for item in self.mealitem_set.all() if item.calculated_fiber is not None)

    @property
    def total_sugar(self):
        return sum(item.calculated_sugar for item in self.mealitem_set.all() if item.calculated_sugar is not None)

    @property
    def total_sodium(self):
        return sum(item.calculated_sodium for item in self.mealitem_set.all() if item.calculated_sodium is not None)

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        ordering = ['-created_at']



# Junction table for Many-to-Many relationship between Meal and Food, storing quantity
class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="Meal")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name="Food")

    # How much of the food was consumed
    # number_of_servings: If Food.serving_unit is "piece" and user ate 2 eggs, number_of_servings = 2
    #                     If Food.serving_unit is "g" and Food.serving_quantity is 100g,
    #                     and user ate 150g, then number_of_servings = 1.5 (i.e., 1.5 * Food.serving_quantity)
    number_of_servings = models.FloatField(
        default=1.0, 
        validators=[MinValueValidator(0.01)], 
        verbose_name="Number of Servings" # e.g., 0.5, 1, 2 servingsj
    )

    @property
    def calculated_calories(self):
        if self.food.calories is not None:
            return self.food.calories * self.number_of_servings
        return None

    @property
    def calculated_protein(self):
        if self.food.protein is not None:
            return self.food.protein * self.number_of_servings
        return None
    
    @property
    def calculated_carbohydrates(self):
        if self.food.carbohydrates is not None:
            return self.food.carbohydrates * self.number_of_servings
        return None
    
    @property
    def calculated_fat(self):
        if self.food.fat is not None:
            return self.food.fat * self.number_of_servings
        return None
    
    @property
    def calculated_fiber(self):
        if self.food.fiber is not None:
            return self.food.fiber * self.number_of_servings
        return None

    @property
    def calculated_sugar(self):
        if self.food.sugar is not None:
            return self.food.sugar * self.number_of_servings
        return None

    @property
    def calculated_sodium(self):
        if self.food.sodium is not None:
            return self.food.sodium * self.number_of_servings
        return None
    
    def __str__(self):
        return f"{self.number_of_servings} x {self.food.name} (in {self.meal.name})"

    class Meta:
        verbose_name = "Meal Item"
        verbose_name_plural = "Meal Items"
        unique_together = ('meal', 'food') # Should increase quantity rather than adding the same food multiple times to one meal

    

class MealPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mealplan')
    name = models.CharField(max_length=150, verbose_name="Meal Plan Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    goal = models.CharField(
        max_length=2,
        choices=MealPlanGoal.choices,
        default=MealPlanGoal.GENERAL_HEALTH,
        verbose_name="Plan Goal"
    )
    duration_days = models.PositiveIntegerField(default=7, verbose_name='Plan Duration (days)')
    start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
    # Desired daily nutrition (optional)
    target_daily_calories = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Target Daily Calories")
    target_daily_protein = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Target Daily Protein (g)")
    target_daily_carbohydrates = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Target Daily Carbohydrates (g)")
    target_daily_fat = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Target Daily Fat (g)")

    meals = models.ManyToManyField(Meal, through='ScheduledMeal', related_name='meal_plans_containing', verbose_name="Meals")
    is_active = models.BooleanField(default=True, verbose_name="Is Plan Active?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.duration_days} days)"
    
    class Meta:
        verbose_name = "Meal Plan"
        verbose_name_plural = "Meal Plans"
        ordering = ['user', '-created_at']
