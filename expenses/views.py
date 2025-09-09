from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest
from .models import Expense

# Create your views here.
@login_required
def traveller_expense_list(request: HttpRequest):
    user = request.user
    expenses = Expense.objects.filter(user_id=user)
    context = {
        'expenses': expenses,
    }
    return render(request, 'expenses/traveller_expense_list.html', context)

@login_required
def approver_expense_list(request: HttpRequest):
    filter_type = request.GET.get('filter', 'new')
    if filter_type == 'past':
        expenses = Expense.objects.filter(status__in=['approved', 'rejected']).order_by('-date')
        page_title = 'Past expenses'
    else:
        expenses = Expense.objects.filter(status='pending').order_by('-date')
        page_title = 'New expenses'
    context = {
        'expenses': expenses,
        'filter_type': filter_type,
        'page_title': page_title
    }
    return render(request, 'expenses/approver_expense_list.html', context)