from django.urls import path
from . import views 

app_name = 'expenses'

urlpatterns = [
    path('traveller/', views.traveller_expense_list, name='traveller_expense_list'),
    path('approver/', views.approver_expense_list, name='approver_expense_list'),
]