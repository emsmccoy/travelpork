from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def assign_permissions_to_groups(apps, schema_editor):
    travellers_group, _ = Group.objects.get_or_create(name='Travellers')
    approvers_group, _ = Group.objects.get_or_create(name='Approvers')
    User = apps.get_model('users', 'CustomUser')
    Expense = apps.get_model('expenses', 'Expense')
    user_ct = ContentType.objects.get_for_model(User)
    expense_ct = ContentType.objects.get_for_model(Expense)
    can_access_traveller, _ = Permission.objects.get_or_create(
        codename='can_access_traveller_dashboard',
        content_type=user_ct,
        defaults={'name': 'Can access traveller dashboard'}
    )
    can_access_approver, _ = Permission.objects.get_or_create(
        codename='can_access_approver_dashboard',
        content_type=user_ct,
        defaults={'name': 'Can access approver dashboard'}
    )
    can_edit_own, _ = Permission.objects.get_or_create(
        codename='can_edit_own_expense',
        content_type=expense_ct,
        defaults={'name': 'Can edit own expenses'}
    )
    can_approve, _ = Permission.objects.get_or_create(
        codename='can_approve_expense',
        content_type=expense_ct,
        defaults={'name': 'Can approve expenses'}
    )
    can_view_all, _ = Permission.objects.get_or_create(
        codename='can_view_all_expenses',
        content_type=expense_ct,
        defaults={'name': 'Can view all expenses'}
    )
    travellers_group.permissions.add(can_access_traveller, can_edit_own)
    approvers_group.permissions.add(can_access_approver, can_approve, can_view_all)

def remove_permissions_from_groups(apps, schema_editor):
    travellers_group = Group.objects.get(name='Travellers')
    approvers_group = Group.objects.get(name='Approvers')
    travellers_group.permissions.clear()
    approvers_group.permissions.clear()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_alter_customuser_options'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(
            assign_permissions_to_groups,
            remove_permissions_from_groups
        ),
    ]