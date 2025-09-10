from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from users.forms import ExpenseForm
from django.db.models import Sum  

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
    all_expenses = Expense.objects.all()
    stats = {
        'pending_count': all_expenses.filter(status='pending').count(),
        'approved_count': all_expenses.filter(status='approved').count(),
        'rejected_count': all_expenses.filter(status='rejected').count(),
        'total_amount': all_expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
    }
    if filter_type == 'past':
        expenses = Expense.objects.filter(status__in=['approved', 'rejected']).order_by('-submission_date')
        page_title = 'Past expenses'
    else:
        expenses = Expense.objects.filter(status='pending').order_by('-submission_date')
        page_title = 'New expenses'
    context = {
        'expenses': expenses,
        'filter_type': filter_type,
        'page_title': page_title,
        'stats': stats,
    }
    return render(request, 'expenses/expense_list_approver.html', context)

# @login_required
# def create_expense(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user_id = request.user
#             expense.status = "pending"
#             expense.save()
#             return redirect('users:traveller_dashboard')
#     else:
#         form = ExpenseForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'expenses/create_expense.html', context)

@login_required
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
def expense_edit_traveller(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.user_id != request.user or not request.user.is_traveller():
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if expense.status != 'pending':
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense) # creates a form (values = input from user) bound to existing expense object
        if form.is_valid():
            expense = form.save(commit=False) # updates existing expense object with form data without saving it in DB
            expense.is_modified = True # set is_modified field to true
            expense.save() # saves modified expense object in DB
            return redirect('expenses:expense_detail', expense_id=expense_id)
    else:
        form = ExpenseForm(instance=expense)
    context = {
        'expense': expense,
        'edit_expense_form': form,
    }
    return render(request, 'expenses/expense_edit_traveller.html', context)

@login_required
def expense_update_approver(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if not request.user.is_approver():
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('approvers_comment', '')
        if action == 'approve':
            expense.status = 'approved'
        elif action == 'reject':
            expense.status = 'rejected'
        expense.approvers_comment = comment
        expense.save()
        return redirect('users:approver_dashboard')
    context = {
        'expense': expense,
        'user_type': 'approver',
    }
    return render(request, 'expenses/expense_detail.html', context)

@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if not request.user.is_traveller() or expense.user_id != request.user:
        return redirect('expenses: expense_list_traveller', expense_id=expense_id)
    if expense.status != 'pending':
        return redirect('expenses: expense_list_traveller', expense_id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expenses:expense_list_traveller')
    context = {
        'expense': expense,
    }
    return render(request, 'expenses/expense_delete_confirm.html', context)