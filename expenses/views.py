from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest
from .models import Expense

# Create your views here.
@login_required
def traveller_expense_list(request: HttpRequest):
    user = request.user
    if user.is_traveller():
        expenses = Expense.objects.filter(user_id=user)
        user_type = 'traveller'
    elif user.is_approver():
        expenses = Expense.objects.all().order_by('status')
        user_type = 'approver'
    else:
        expenses = Expense.objects.none()
        user_type = 'unknown'
    context = {
        'user': user,
        'user_type': user_type,
        'expenses': expenses,
    }
    return render(request, 'expenses/traveller_expense_list.html', context)