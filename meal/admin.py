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

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'meal_time_category', 'total_calories_display','total_protein_display','total_carbohydrates_display','total_fat_display', 'is_template', 'created_at')
    list_filter = ('meal_time_category', 'user', 'is_template')
    search_fields = ('name', 'user__username', 'description')
    inlines = [MealItemInline]
    readonly_fields = ('total_calories', 'total_protein', 'total_carbohydrates', 'total_fat')
    def total_calories_display(self, obj):
        return obj.total_calories
    total_calories_display.short_description = "Total Calories"
    def total_protein_display(self, obj):
        return obj.total_protein
    total_protein_display.short_description = "Total Protein"

    def total_carbohydrates_display(self, obj):
        return obj.total_carbohydrates
    total_carbohydrates_display.short_description = "Total Carbohydrates"

    def total_fat_display(self, obj):
        return obj.total_fat
    total_fat_display.short_description = "Total Fat"

class ScheduledMealInline(admin.TabularInline):
    model = ScheduledMeal
    extra = 1
    autocomplete_fields = ['meal'] # For easier searching if you have many Meal items

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'goal', 'duration_days', 'is_active', 'start_date', 'is_template')
    list_filter = ('goal', 'user', 'is_active')
    search_fields = ('name', 'user__username', 'description')
    inlines = [ScheduledMealInline]
    fieldsets = (
        (None, { 
            'fields': ('user', 'name', 'description', 'goal')
        }),
        ('Plan Details', {
            'fields': ('duration_days', 'start_date', 'is_active')
        }),
        ('Target Nutrition (Optional)', {
            'classes': ('collapse',), # Collapsed by default
             # Add other target nutrients here
             'fields': ('target_daily_calories', 'target_daily_protein', 'target_daily_carbohydrates', 'target_daily_fat')
        }),
    )