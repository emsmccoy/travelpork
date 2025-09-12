# TravelPork
A Django-based expense management system designed to handle travel and business expense submissions, reviews, and approvals.

## Overview
### For Travellers
- **Expense Submission**: Submit expenses with details including date, amount, category, and description
- **Expense Management**: List and view all own expenses, and edit and delete pending expenses
- **Status Tracking**: Monitor approval status of submitted expenses. Get a notification in dashboard when status changed
- **Dashboard**: Overview of expense statistics and quick expense submission

### For Approvers
- **Expense Review**: Review all submitted expenses from team members
- **Approval Workflow**: Approve or reject expenses with comments
- **Filtering**: View expenses by status (new/pending vs. past/processed)
- **Analytics**: View expense statistics and totals

### System Features
- **Role-based Access**: Separate interfaces for travellers and approvers
- **Expense Categories**: Accommodation, Flights, Trains, Cars, Meals, Others
- **Modification Tracking**: Track when expenses have been modified
- **Secure Authentication**: User login/logout with role-based permissions

### Technology Stack
- **Backend**: Django 5.2.6
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, Django Templates
- **Authentication**: Django's built-in auth system with custom user model


## How to run this app
### Prerequisites
- Python 3.11+
- pip

### Setup
1. **Clone the repository**
```bash
git clone https://github.com/emsmccoy/travelpork.git
cd travelpork
```

2. **Create and activate virtual environment with Python version 3.11.5**
```bash
pyenv virtualenv 3.11.5 travelpork-env
pyenv activate travelpork-env
```

3. **Install Django**
```bash
pip install django
```

4. **Database setup and creation of 'travellers' and 'approvers' groups**
```bash
python manage.py migrate
```

5. **Seed test data (optional)**
```bash
python manage.py seed_expenses
```

6. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## Usage

### First Time Setup

1. Create a superuser:
```bash
python manage.py createsuperuser
```

2. Access admin panel at `/admin/` to:
   - Create user accounts
   - Assign users to groups (Travellers or Approvers)

### Test Accounts

If you've run the seeder, you can login with:

**Travellers:**
- Username: `john_traveller` | Password: `qwerty123`
-> 3 expenses: pending, approved and rejected.

- Username: `jane_traveller` | Password: `qwerty123`
-> 3 expenses: approved, pending and pending

**Approver:**
- Username: `boss_approver` | Password: `qwerty123`
-> New expenses: 3 / Past expenses: 3

### User Workflows

#### Traveller Workflow
1. Login → Redirected to traveller dashboard
2. Submit new expenses using the form
3. Check status report at 'Quick summary'
4. View expense list by clicking at 'Manage all expenses'
5. View details of all expenses and edit pending expenses
6. Monitor approval status

#### Approver Workflow
1. Login → Redirected to approver dashboard
2. Check new expenses listed under the 'Pending expenses' tab
3. Review details of pending expenses and approve or reject them with comments
4. View all processed expenses by clicking at 'Past expenses' tab

## API Endpoints

### Authentication
- `GET /` - Login page
- `POST /accounts/logout/` - Logout

### Users dashboards
- `GET /users/redirect/` - Role-based redirection
- `GET /users/traveller-dashboard/` - Traveller dashboard
- `GET /users/approver-dashboard/` - Approver dashboard (approver expense list)

### Expenses
- `POST /expenses/create` - Create 
- `GET /expenses/list/traveller/` - Traveller expense list
- `GET /expenses/<id>/detail/` - Expense details (for both travellers and approvers)
- `GET|POST /expenses/<id>/edit/` - Edit expense (for travellers only)
- `POST /expenses/<id>/approve/` - Approve/reject expense (for approvers only)
- `GET|POST /expenses/<id>/delete/` - Delete expense (for travellers only)

## Database Schema

### CustomUser Model
- Extends Django's AbstractUser
- Additional fields: position, date of birth, passport, account_number
- Helper methods: `is_traveller()`, `is_approver()`

### Expense Model
- **expense_date**: Date when expense occurred
- **submission_date**: When expense was submitted (auto-set)
- **amount**: Decimal field for expense amount
- **category**: Choice field (accommodation, flights, trains, cars, meals, others)
- **description**: Text description
- **status**: Choice field (pending, approved, rejected)
- **user_id**: Foreign key to CustomUser
- **approvers_comment**: Optional comment from approver
- **is_modified**: Boolean flag for tracking modifications

## Testing

Run the test suite:
```bash
python manage.py test
```

The test suite includes:
- Expense list view functionality tests
- Role-based access control (traveller vs approver permissions)  
- User data isolation (travellers see only own expenses)
- Authentication requirement enforcement
- Template rendering verification
- Expense status filtering for approvers

## Development

### Project Structure
```
travelpork/
├── expenses/           # Expense management app
├── users/             # User management app
├── templates/         # Project-level templates
├── static/           # CSS and static files
├── travelpork/       # Project settings
└── manage.py
```

### Key Management Commands
- `python manage.py seed_expenses` - Populate test data
- `python manage.py flush` - Clear database
- `python manage.py test` - Run tests

### Development Workflow
1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes and test
3. Run tests: `python manage.py test`
4. Commit and push changes
5. Create pull request

## Security Considerations

- SECRET_KEY should be changed for production
- DEBUG should be False in production
- Configure ALLOWED_HOSTS for production
- Use environment variables for sensitive settings
- Implement proper database for production (PostgreSQL recommended)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request