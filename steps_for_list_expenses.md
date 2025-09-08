## 1- Add expenses urls to travelpork/urls.py
```
path('expenses/', include('expenses.urls')),
```

## 2- Create travelpork/expenses/urls.py
```
from django.urls import path
from . import views 

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list, 'expense_list'),
]
```

## 3- Create travelpork/expenses/management/commands directories

## 4- Create and argument travelpork/expenses/management/commands/see_expenses.py

## 5- Create tests for traevlpork/expenses/views/list_expenses() in travelpork/expenses/tests.py 

## 6- Argument traevlpork/expenses/views/list_expenses()

## 7- Make migrations and migrate (to add 'approvers_comment column) and populate the DB
```
python manage.py makemigrations
python manage.py migrate
python manage.py seed_expenses
```

## 8- Create and fill templates
