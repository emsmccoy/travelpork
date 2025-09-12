from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages  
from django.db.models import Sum     
from expenses.models import Expense  
from expenses.forms import ExpenseForm
from expenses.views import expense_create  


# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_traveller():
        return redirect('users:traveller_dashboard')
    elif user.is_approver():
        return redirect('users:approver_dashboard')
    else:
        return redirect('users:default_dashboard')

@login_required
def traveller_dashboard(request):
    user_expenses = Expense.objects.filter(user_id=request.user) # to retrieve the expense descriptions 
    
    # To show stats on the dashboard
    stats = {
        'total_expenses': user_expenses.count(),
        'total_amount': user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_count': user_expenses.filter(status='pending').count(),
        'approved_count': user_expenses.filter(status='approved').count(),  
        'rejected_count': user_expenses.filter(status='rejected').count(),   
    }

    # keep expense creation logic in the expenses app
    is_expense_created, form = expense_create(request)
    if is_expense_created:
        return redirect('users:traveller_dashboard') 
    
    context = {
        'stats': stats,
        'form': form,
        'user_expenses': user_expenses,  
    }
    
    return render(request, 'dashboard/traveller_dashboard.html', context)

@login_required
def approver_dashboard(request):
    filter_type = request.GET.get('filter', 'new')
    all_expenses = Expense.objects.all()
    stats = {
        'pending_count': all_expenses.filter(status='pending').count(),
        'approved_count': all_expenses.filter(status='approved').count(),
        'rejected_count': all_expenses.filter(status='rejected').count(),
        'total_amount': all_expenses.filter(status='approved').aggregate(Sum('amount'))['amount__sum'] or 0,
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
    return render(request, 'dashboard/approver_dashboard.html', context)


@login_required
def default_dashboard(request):
    return render(request, 'dashboard/default_dashboard.html')