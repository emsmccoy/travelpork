from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'expense_date']
        widgets = {
            'expense_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the expense (e.g., lunch with client)'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }