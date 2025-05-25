from django.db import models
from django.conf import settings


class Meal(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    recipe = models.CharField(max_length=50)
    mealtime = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.mealtime}"

class MealPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mealplan')
    meal = models.ManyToManyField(Meal, related_name='meal')
    date = models.DateField()
    total_calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    is_ai_generated = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user}"
    
