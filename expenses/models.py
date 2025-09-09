from django.db import models
from django.utils import timezone
from users.models import CustomUser

# Create your models here.
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('flights', 'Flights'),
        ('trains', 'Trains'),
        ('cars', 'Cars'),
        ('meals', 'Meals'),
        ('others', 'Others'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    expense_date = models.DateField() 
    submission_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=300)
    status = models.CharField(choices=STATUS_CHOICES)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expenses')
    approvers_comment = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return f'Expense\nUser id: {self.user_id}\nAmount: {self.amount}\nExpense date: {self.date}\nStatus: {self.status}'
    
    class Meta:
        ordering = ['-submission_date']