from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def dashboard_redirect(request):
    if request.user.groups.filter(name='Approvers').exists():
        return redirect('approver_dashboard')
    elif request.user.groups.filter(name='Travellers').exists():
        return redirect('traveller_dashboard')
    else:
        return redirect('default_dashboard')
    
@login_required
def approver_dashboard(request):
    return render(request, 'approver_dashboard.html')

@login_required
def traveller_dashboard(request):
    return render(request, 'traveller_dashboard.html')

@login_required
def default_dashboard(request):
    return render(request, 'default_dashboard.html')