from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.management import call_command
from users.models import CustomUser
from expenses.models import Expense

# Create your tests here.
class ExpenseListViewTests(TestCase):
    def setUp(self):
        Expense.objects.all().delete()
        CustomUser.objects.filter(username__in=['john_traveller', 'jane_traveller', 'boss_approver']).delete()
        call_command('seed_expenses')
        self.client = Client()
        self.john = CustomUser.objects.get(username='john_traveller')
        self.jane = CustomUser.objects.get(username='jane_traveller')
        self.boss = CustomUser.objects.get(username='boss_approver')
    
    def test_traveller_sees_only_own_expenses(self):
        self.client.force_login(self.john)
        response = self.client.get(reverse('expenses:expense_list_traveller'))
        self.assertEqual(response.status_code, 200)
        expenses_in_context = response.context['expenses']
        self.assertEqual(expenses_in_context.count(), 3)
        for expense in expenses_in_context:
            self.assertEqual(expense.user_id, self.john)
                
    def test_different_traveller_sees_different_expenses(self):
        self.client.force_login(self.jane)
        response = self.client.get(reverse('expenses:expense_list_traveller'))
        self.assertEqual(response.status_code, 200)
        expenses_in_context = response.context['expenses']
        self.assertEqual(expenses_in_context.count(), 3)
        for expense in expenses_in_context:
            self.assertEqual(expense.user_id, self.jane)

    def test_approver_sees_all_pending_expenses(self):
        self.client.force_login(self.boss)
        response = self.client.get(reverse('users:approver_dashboard'))
        expenses_in_context = response.context['expenses']
        pending_count = Expense.objects.filter(status='pending').count()
        self.assertEqual(expenses_in_context.count(), pending_count)
    
    def test_approver_sees_all_processed_expenses(self):
        self.client.force_login(self.boss)
        response = self.client.get(reverse('users:approver_dashboard'))
        expenses_in_context = response.context['expenses']
        pending_count = Expense.objects.filter(status__in=['approved', 'rejected']).count()
        self.assertEqual(expenses_in_context.count(), pending_count)
        
    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('users:approver_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
        
    def test_traveller_cannot_see_other_traveller_expenses(self):
        self.client.force_login(self.john)
        response = self.client.get(reverse('expenses:expense_list_traveller'))
        expenses_in_context = response.context['expenses']
        for expense in expenses_in_context:
            self.assertNotEqual(expense.user_id, self.jane)
            
    def test_page_uses_correct_template(self):
        self.client.force_login(self.john)
        response = self.client.get(reverse('expenses:expense_list_traveller'))
        self.assertTemplateUsed(response, 'expenses/expense_list_traveller.html')