from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField 

# Create your models here.
class CustomUser(AbstractUser):
    position = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    passport = models.CharField(max_length=10, blank=True, null=True)
    account_number = models.CharField(max_length=15, blank=True, null=True)
    session_data = JSONField(default=dict, blank=True)

    def is_traveller(self):
        return self.groups.filter(name='Travellers').exists()
    
    def is_approver(self):
        return self.groups.filter(name='Approvers').exists()

    def __str__(self):
        return f'User\nName: {self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['last_name']
        permissions = [
            ('can_access_traveller_dashboard', "Can access traveller dashboard"),
            ('can_access_approver_dashboard', "Can access approver dashboard"),
        ]