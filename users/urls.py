from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('traveller-dashboard/', views.traveller_dashboard, name='traveller_dashboard'),
    path('approver-dashboard/', views.approver_dashboard, name='approver_dashboard'),
]