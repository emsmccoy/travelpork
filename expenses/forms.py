from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'description', 'expense_date']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'What did you spend money on?'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }