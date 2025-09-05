## 1- Define permissions on Expense model (each permission is a tuple):
```
class Expense(models.Model):
    # your fields here
    
    class Meta:
        permissions = [
            ("permission_codename", "Human readable description"),
            ("can_approve_expenses", "Can approve expenses"),
            ("can_view_all_expenses", "Can view all expenses"),
            ("can_delete_expenses", "Can delete expenses"),
        ]
```

## 2- Create the migration file
```
python manage.py makemigrations users --empty
```

## 3- Complete the new data migration file
```
from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name='Travellers')
    Group.objects.get_or_create(name='Approvers')

def assign_permissions(apps, schema_editor):
   travellers = Group.objects.get(name='Travellers')
   approvers = Group.objects.get(name='Approvers')
   
   approve_perm = Permission.objects.get(codename='can_approve_expenses')
   view_perm = Permission.objects.get(codename='can_view_all_expenses')
   delete_perm = Permission.objects.get(codename='can_delete_expenses')
   
   travellers.permissions.set([])
   approvers.permissions.set([]) 

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_groups),
        migrations.RunPython(assign_permissions),
    ]
```

## 4- Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

## 5- Apply decorators to views:
```
from django.contrib.auth.decorators import permission_required

@permission_required('expenses.can_approve_expenses')
def approve_expense_view(request):
    # This function requires the approve permission
    pass

@permission_required('expenses.can_view_all_expenses') 
def view_all_expenses(request):
    # This function requires the view all permission
    pass
```