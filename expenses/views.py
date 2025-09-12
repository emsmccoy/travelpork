from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import ExpenseForm
from django.db.models import Sum

# Create your views here.
@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user
            expense.status = "pending"
            expense.save()
            return True, ExpenseForm()
        else:
            return False, form
    else:
        return False, ExpenseForm()

@login_required
@permission_required('users.can_access_traveller_dashboard')
def expense_list_traveller(request):
    user = request.user
    expenses = Expense.objects.filter(user_id=user)
    context = {
        'expenses': expenses,
    }
    return render(request, 'expenses/expense_list_traveller.html', context)

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
@permission_required('expenses.can_edit_own_expense')
def expense_edit_traveller(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if expense.user_id != request.user or not request.user.is_traveller():
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if expense.status != 'pending':
        return redirect('expenses:expense_detail', expense_id=expense_id)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense) 
        if form.is_valid():
            expense = form.save(commit=False) 
            expense.is_modified = True 
            expense.save()
            return redirect('expenses:expense_detail', expense_id=expense_id)
    else:
        form = ExpenseForm(instance=expense)
    context = {
        'expense': expense,
        'edit_expense_form': form,
    }
    return render(request, 'expenses/expense_edit_traveller.html', context)

@login_required
@permission_required('expenses.can_approve_expense')
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
        alert = (f'Your expense "{expense.description[:40]}" '
                f'was {expense.status}.')
        tag  = 'approved' if expense.status == 'approved' else 'rejected'
        queue = expense.user_id.session_data.get('_alerts', [])
        queue.append((alert, tag))
        expense.user_id.session_data['_alerts'] = queue
        expense.user_id.save(update_fields=['session_data'])
        return redirect('users:approver_dashboard')
    context = {
        'expense': expense,
        'user_type': 'approver',
    }
    return render(request, 'expenses/expense_detail.html', context)

@login_required
@permission_required('expenses.can_edit_own_expense')
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