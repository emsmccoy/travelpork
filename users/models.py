from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    position = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    passport = models.CharField(max_length=10, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)

    def is_traveller(self):
        return self.groups.filter(name='Travellers').exists()
    
    def is_approver(self):
        return self.groups.filter(name='Approvers').exists()

    def __str__(self):
        return f'User\nName: {self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['last_name']