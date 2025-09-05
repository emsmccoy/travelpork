from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    position = models.CharField(max_length=100)
    dob = models.DateField()
    passport = models.CharField(max_length=10)
    account_number = models.CharField(max_length=15)

    def __str__(self):
        return f'User\nName: {self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['last_name']