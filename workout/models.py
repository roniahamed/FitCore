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
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='photos', blank=True, null=True)
    duration = models.IntegerField()
    order_index = models.IntegerField(default=0)
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_workout_videos')

    def __str__(self):
        return f"{self.title} ({self.workout.title})"