import os
import django

# Set up Django environment to access models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos.settings')
django.setup()

from posApp.models import Role, RoleCategory, CustomUser

def create_roles_and_categories():
    print("Started Creating Roles and Categories")

    # Define categories and their corresponding roles
    categories_and_roles = {
        'Sales': [
            'Make sale below S.P',
            'Sell on Credit',
            'Sell below Selling Price',
            'Delete sales'
        ],
        'User Management': [
            'Can create new users',
            'Can edit roles',
            'Can view users',
            'Can delete users'
        ],
        'Reports': [
            'Generate Sales Reports',
            'View Inventory Reports',
            'Customer Feedback Reports'
        ],
        'Customers': [
            'View Customer List',
            'Edit Customer Details',
            'Delete Customers'
        ],
        'Suppliers': [
            'View Supplier List',
            'Edit Supplier Details',
            'Delete Suppliers'
        ],
        'POS': [
            'Process Sales Transactions',
            'View Daily Sales',
            'Manage Discounts'
        ]
    }

    # Create categories and roles
    for category_name, role_names in categories_and_roles.items():
        category, created = RoleCategory.objects.get_or_create(name=category_name)
        for role_name in role_names:
            Role.objects.get_or_create(name=role_name, category=category)

    print("Roles and categories populated successfully.")

    # Now create the superuser and assign all roles
    create_admin_user()

def create_admin_user():
    print("Started Creating Admin User")

    # Check if admin user already exists
    if not CustomUser.objects.filter(username='admin').exists():
        # Create superuser with username 'admin' and password 'admin'
        admin_user = CustomUser.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

        # Assign all roles to the superuser (assuming roles can be related to users)
        roles = Role.objects.all()  # Fetch all roles

        admin_user.roles.set(roles)
        admin_user.save()
        print(f"Superuser 'admin' created with all roles.")
    else:
        admin_user = CustomUser.objects.get(username='admin')
        # Assign all roles to the superuser (assuming roles can be related to users)
        roles = Role.objects.all()  # Fetch all roles

        admin_user.roles.set(roles)
        admin_user.save()
        print("Admin user has been assigned all roles")

create_roles_and_categories()
