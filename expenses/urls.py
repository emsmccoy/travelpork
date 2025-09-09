from django.urls import path
from . import views 

app_name = 'expenses'

urlpatterns = [
    path('traveller/', views.traveller_expense_list, name='traveller_expense_list'),
    path('approver/', views.approver_expense_list, name='approver_expense_list'),
    path('new/', views.create_expense, name='create_expense'),
    path('<int:expense_id>/detail/', views.expense_detail, name='expense_detail'),
    path('<int:expense_id>/edit/', views.expense_edit, name='expense_edit'),
    path('<int:expense_id>/update/', views.expense_update, name='expense_update'),
]