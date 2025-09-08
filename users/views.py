from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages  
from django.db.models import Sum     
from expenses.models import Expense  
from .forms import ExpenseForm  

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_traveller():
        return redirect('expenses:expense_list')
    elif user.is_approver():
        return redirect('expenses:expense_list')
    else:
        return redirect('default_dashboard')
<<<<<<< HEAD
=======
    
@login_required
def approver_dashboard(request):
    return render(request, 'dashboard/approver_dashboard.html')

@login_required
def traveller_dashboard(request):
    user_expenses = Expense.objects.filter(user_id=request.user)
    
    # stats calculation
    stats = {
        'total_expenses': user_expenses.count(),
        'total_amount': user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_count': user_expenses.filter(status='pending').count(),
    }
    
    # add expense form
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user_id = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('traveller_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExpenseForm()
    
    context = {
        'stats': stats,
        'form': form,
    }
    return render(request, 'dashboard/traveller_dashboard.html', context)
>>>>>>> f3295f1 (Add traveller dashboard)

@login_required
def default_dashboard(request):
    return render(request, 'dashboard/default_dashboard.html')