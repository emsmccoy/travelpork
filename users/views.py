from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

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

@login_required
def default_dashboard(request):
    return render(request, 'dashboard/default_dashboard.html')