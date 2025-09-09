from django.urls import path
from . import views 

app_name = 'expenses'

urlpatterns = [
    path('create/', views.create_expense, name='expense_create'),
    path('list/traveller/', views.expense_list_traveller, name='expense_list_traveller'),
    path('list/approver/', views.expense_list_approver, name='expense_list_approver'),
    path('<int:expense_id>/detail/', views.expense_detail, name='expense_detail'),
    # path('<int:expense_id>/edit/', views.expense_edit_traveller, name='expense_edit'),
    # path('<int:expense_id>/approve/', views.expense_update_approver, name='expense_approve'),
]