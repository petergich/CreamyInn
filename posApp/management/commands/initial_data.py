


# Import models
from django.core.management.base import BaseCommand
from posApp.models import Role, RoleCategory, CustomUser

class Command(BaseCommand):
    help = 'Populates roles and categories'

    def handle(self, *args, **kwargs):
        # Copy your `create_roles_and_categories` logic here
        print("Populating roles and categories...")
        create_roles_and_categories()

        print("Done.")

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
    create_admin_user()


def create_admin_user():
    print("Started Creating Admin User")

    # Check if admin user already exists
    if not CustomUser.objects.filter(username='admin').exists():
        admin_user = CustomUser.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com'
        )

        # Assign all roles to the admin user
        roles = Role.objects.all()
        admin_user.roles.set(roles)
        admin_user.save()
        print("Superuser 'admin' created with all roles.")
    else:
        print("Admin user already exists.")
        admin_user = CustomUser.objects.get(username='admin')

        # Ensure admin has all roles
        roles = Role.objects.all()
        admin_user.roles.set(roles)
        admin_user.save()
        print("Admin user has been assigned all roles.")

# Call the function directly

