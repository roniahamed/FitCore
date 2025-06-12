from django.contrib import admin
from .models import Meal, MealPlan, Food, MealItem, ScheduledMeal


class MealItemInline(admin.TabularInline):
    model = MealItem
    extra = 1 # Default number of empty from to display 
    autocomplete_fields = ['food'] # For easier searching if you have many food items

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'serving_quantity', 'serving_unit', 'calories', 'protein', 'carbohydrates', 'fat', 'food_category', 'user_added', 'is_public')
    list_filter = ('food_category', 'is_public', 'user_added')
    search_fields = ('name', )
    fieldsets = (
        (None ,{
            'fields':('name', 'description', 'food_category', )
        }),
        ( 'Serving & Nutrition', {
            'fields': (('serving_quantity', 'serving_unit'), ('calories', 'protein'), ('carbohydrates', 'fat'), ('fiber', 'sugar', 'sodium'))
        }),
        ('User & Visibility', {
            'fields' : ('user_added', 'is_public')
        })
    )

