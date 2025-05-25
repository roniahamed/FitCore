from django.db import models
from users.models import CustomUser

class HealthData(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='healthdata')
    data_type = models.CharField(max_length=100)
    value = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    harte_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.data_type} - {self.recorded_at}"