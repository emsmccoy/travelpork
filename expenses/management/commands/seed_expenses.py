from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from expenses.models import Expense
from users.models import CustomUser
from decimal import Decimal
from datetime import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed database with test expenses for Travellers and Approvers'
    
    def handle(self, *args, **options):
        # get groups
        travellers_group = Group.objects.get(name='Travellers')
        approvers_group = Group.objects.get(name='Approvers')
        # create test travellers
        traveller1, _ = CustomUser.objects.get_or_create(
            username='john_traveller',
            defaults={
                'email': 'john@company.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'position': 'Sales Representative',
                'dob': '1990-05-15',
                'passport': 'A1234567',
                'account_number': '1234567890123'
            }
        )
        traveller1.set_password('qwerty123')
        traveller1.save() 
        traveller1.groups.add(travellers_group)
        traveller2, _ = CustomUser.objects.get_or_create(
            username='jane_traveller',
            defaults={
                'email': 'jane@company.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'position': 'Marketing Manager',
                'dob': '1988-08-22',
                'passport': 'B9876543',
                'account_number': '9876543210987'
            }
        )
        traveller2.set_password('qwerty123')
        traveller2.save() 
        traveller2.groups.add(travellers_group)
        # create test approver
        approver1, _ = CustomUser.objects.get_or_create(
            username='boss_approver',
            defaults={
                'email': 'boss@company.com',
                'first_name': 'Robert',
                'last_name': 'Manager',
                'position': 'Regional Director',
                'dob': '1975-03-10',
                'passport': 'C1122334',
                'account_number': '5555666677778'
            }
        )
        approver1.set_password('qwerty123')
        approver1.save() 
        approver1.groups.add(approvers_group)
        # expenses for traveller1
        john_expenses = [
            {
                'date': timezone.make_aware(datetime(2025, 1, 15, 14, 30)),
                'amount': Decimal('125.50'),
                'category': 'accommodation',
                'description': 'Hotel stay in Madrid for client meeting',
                'status': 'pending',
                'user_id': traveller1,
                'approvers_comment': None
            },
            {
                'date': timezone.make_aware(datetime(2025, 1, 16, 19, 45)),
                'amount': Decimal('67.80'),
                'category': 'meals',
                'description': 'Business dinner with potential client',
                'status': 'approved',
                'user_id': traveller1,
                'approvers_comment': 'Approved - Good networking opportunity'
            },
            {
                'date': timezone.make_aware(datetime(2025, 1, 17, 8, 15)),
                'amount': Decimal('45.00'),
                'category': 'cars',
                'description': 'Taxi to airport',
                'status': 'rejected',
                'user_id': traveller1,
                'approvers_comment': 'Please use company shuttle service'
            }
        ] 
        # expenses for traveller2
        jane_expenses = [
            {
                'date': timezone.make_aware(datetime(2025, 1, 10, 6, 30)),
                'amount': Decimal('320.00'),
                'category': 'flights',
                'description': 'Round trip flight to Barcelona for conference',
                'status': 'approved',
                'user_id': traveller2,
                'approvers_comment': 'Conference attendance approved'
            },
            {
                'date': timezone.make_aware(datetime(2025, 1, 11, 12, 00)),
                'amount': Decimal('89.50'),
                'category': 'trains',
                'description': 'Train from airport to city center',
                'status': 'pending',
                'user_id': traveller2,
                'approvers_comment': None
            },
            {
                'date': timezone.make_aware(datetime(2025, 1, 12, 20, 30)),
                'amount': Decimal('156.75'),
                'category': 'others',
                'description': 'Conference registration fee',
                'status': 'pending',
                'user_id': traveller2,
                'approvers_comment': None
            }
        ]
        # create all expenses
        all_expenses = john_expenses + jane_expenses 
        for expense_data in all_expenses:
            expense, created = Expense.objects.get_or_create(
                date=expense_data['date'],
                user_id=expense_data['user_id'],
                description=expense_data['description'],
                defaults=expense_data
            )