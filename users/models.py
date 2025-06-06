from django.contrib.auth.models import AbstractUser 
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

Choices = [('male','Male'), ('female','Female')]


class UsersProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    img = models.ImageField(upload_to='profile', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    weight = models.FloatField(help_text="Weight in kg", blank=True,null=True)
    height = models.FloatField(help_text="Height in cm" , blank=True,null=True)
    gender = models.CharField(max_length=10,choices=Choices, blank=True,null=True)
    fitness_goal = models.CharField(max_length=200 , blank=True,null=True)

    def __str__(self):
        return f'{self.user.email} - {self.fitness_goal}'

