from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Expense
from expenses.forms import ExpenseForm

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

@login_required
def create_expense(request: HttpRequest):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user
            expense.status = "pending"
            form.save()
            return redirect('users:traveller_dashboard')
    else:
        form = ExpenseForm()
    
    context = {
        'form': form
        }
    return render(request, 'expenses/create_expense.html', context)
def expense_edit(request: HttpRequest, expense_id):
    user = request.user
    # if user is traveller
        # show form to allow to modify everything except status
    # if user is approver
        # show form to allow to modify status and add approver's comment
pass

@login_required
def expense_update(request: HttpRequest, expense_id):
    user = request.user
    # if updated_expense is valid
        # store expense
pass
