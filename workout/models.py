from django.utils import timezone
from django.db import models
from django.conf import settings


class Workout(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.FloatField()
    difficulty = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    goals = models.CharField(max_length=100)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.duration}"


class WorkoutVideo(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='workoutvideo' )
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='photos', blank=True, null=True)
    duration = models.IntegerField()
    order_index = models.IntegerField(default=0)
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workoutvideo')

    def __str__(self):
        return f"{self.title} ({self.workout.title})"
    

class WorkOutProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress' )
    workout = models.ManyToManyField(Workout, related_name='progress')
    completed_at = models.DateTimeField(default=None, null=True, blank=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s progress on {self.workout.name}: {self.progress_percentage}%"
    
    def save(self, *args, **kwargs):
        if self.progress_percentage == 100 and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.progress_percentage < 100 and self.completed_at is not None:
            self.completed_at = None
        super().save(*args, **kwargs)