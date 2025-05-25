from django.contrib import admin
from .models import Workout, WorkoutVideo

@admin.register(WorkoutVideo)
class WorkoutVideoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_staff
    
    def save_model(self,request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Workout)