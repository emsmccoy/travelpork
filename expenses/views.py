from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from expenses.forms import ExpenseForm

# Create your views here.
@login_required
def expense_list_traveller(request):
    user = request.user
    expenses = Expense.objects.filter(user_id=user)
    context = {
        'expenses': expenses,
    }
    return render(request, 'expenses/expense_list_traveller.html', context)

@login_required
def expense_list_approver(request):
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
    return render(request, 'expenses/expense_list_approver.html', context)

@login_required
def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user
            expense.status = "pending"
            expense.save()
            return redirect('users:traveller_dashboard')
    else:
        form = ExpenseForm()
    context = {
        'form': form
    }
    return render(request, 'expenses/create_expense.html', context)

def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    user = request.user
    if user.is_approver():
        user_type = 'approver'
    else:
        user_type = 'traveller'
    context = {
        'expense': expense,
        'user_type': user_type,
    }
    return render(request, 'expenses/expense_detail.html', context)

@login_required
def traveller_expense_edit(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.user_id != request.user or not request.user.is_traveller():
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if expense.status != 'pending':
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if request.method == 'POST':
        expense.amount = re
    context = {
        'expense': expense,
    }
    return render(request, 'expenses/traveller_expense_edit.html', context)

@login_required
def traveller_expense_update(request, expense_id):
    pass

@login_required
def expense_edit(request, expense_id):
    user = request.user
    # if user is traveller
        # show form to allow to modify everything except status
    # if user is approver
        # show form to allow to modify status and add approver's comment
pass

@login_required
def expense_update(request, expense_id):
    user = request.user
    # if updated_expense is valid
        # store expense
pass
