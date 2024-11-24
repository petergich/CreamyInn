from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
#from flask import jsonify
from posApp.models import *
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json, sys
from datetime import date, datetime,timedelta
from django.utils import timezone
from django.db.models import F
from django.http import JsonResponse


# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')
#users
@login_required
def users(request):
    if has_role(request,'Can view users'):
        return render(request,"posApp/users.html",{"users":CustomUser.objects.all()})
    else:
        return redirect("home-page")
@login_required
def manage_users(request):
    user = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            user = CustomUser.objects.filter(id=id).first()
    
    context = {
        'user': user,
        "groups":UserGroup.objects.all()
    }
    return render(request, 'posApp/manage_user.html', context)


@login_required
def save_user(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']

    try:
        if id.isnumeric() and int(id) > 0:
            user = CustomUser.objects.get(id=id)

            if data["username"] == "admin" and user.username != "admin":
                resp['msg'] = "You cannot save a user with this username"
            else:
                # Update user fields
                user.username = data['username']
                user.email = data['email']
                user.name = data['name']
                user.phone = data['phone']
                
                # If password is provided, set it properly
                if data['password']:
                    user.set_password(data['password'])  # Encrypt password
                if data["group"]:
                    try:
                        
                        group = UserGroup.objects.get(id=data['group'])
                        user.roles.set(group.roles.all())
                        user.group = group
                    except:
                        pass
                user.save()  # Save the user with the updated details
        else:
            if data["username"] == "admin":
                resp['msg'] = "You cannot create a user with this username"
            else:
                # Create a new user with hashed password
                save_user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    name=data['name'],
                    phone=data['phone'],
                    password=data['password']  # This will be hashed automatically by create_user
                )
                if data["group"]:
                    try:
                        group = UserGroup.objects.get(id=data['group'])
                        save_user.roles.set(group.roles.all())
                        save_user.group = group

                    except:
                        pass
                
                save_user.save()
        
        resp['status'] = 'success'
        messages.success(request, 'User Successfully saved.')
    except Exception as e:
        resp['msg'] = str(e)
        resp['status'] = 'failed'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def user_roles(request):
    resp = {'status': ''}
    if request.method == 'POST':
        data = json.loads(request.body)
        role_ids = data.get('roles', [])
        user = CustomUser.objects.get(id=data.get("user")) 
        roles = Role.objects.filter(id__in=role_ids)
        # Clear old roles and assign new ones
        user.roles.set(roles)
        try:
            role_categories = RoleCategory.objects.all()
            roles = Role.objects.all() 
            resp['status'] = 'success'
            messages.success(request, 'Roles successfully updated.')
            return HttpResponse(json.dumps(resp), content_type="application/json")
        except:
            return redirect("users")
    else:
        data = request.GET
        try:
            user = CustomUser.objects.get(id=data['id'])
            role_categories = RoleCategory.objects.all()
            roles = Role.objects.all() 
            return render(request, "posApp/user_roles.html",{"user":user,"rolecategories":role_categories,"roles":roles})
        except:
            return redirect("users")
@login_required
def delete_user(request):
    data = request.POST
    resp = {'status': ''}
    try:
        CustomUser.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'User Successfully deleted.')
    except Exception as e:
        resp['msg'] = str(e)
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
def has_role(request,role):
    try:
        role = Role.objects.get(name = role)
        user = request.user
        if role in user.roles.all():
            print("Found")
            return True
        else:
            print("Not Found")
            return False
    except:
        print("An Error occured")
        return False
#user groups
@login_required
def groups(request):
    return render(request,"posApp/groups.html",{"groups":UserGroup.objects.all()})
@login_required
def manage_groups(request):
    group = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            group = UserGroup.objects.filter(id=id).first()
    
    context = {
        'group': group,
    }
    return render(request, 'posApp/manage_group.html', context)


@login_required
def save_group(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']

    try:
        if id.isnumeric() and int(id) > 0:
            group = UserGroup.objects.get(id=id)
            # Update group fields
            group.description = data['description']
            group.name = data['name']
            group.save()  # Save the group with the updated details
        else:
            # Create a new user with hashed password
            save_group = UserGroup.objects.create(
                name = data["name"],
                description = data["description"]
            )
            save_group.save()
        
        resp['status'] = 'success'
        messages.success(request, 'Group succesfully saved.')
    except Exception as e:
        resp['msg'] = str(e)
        resp['status'] = 'failed'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

def group_roles(request):
    data = request.GET
    if request.method == 'POST':
        data = json.loads(request.body)
        role_ids = data.get('roles', [])
        print(data.get("group"))
        # Assuming you want to assign the roles to a group
        group = UserGroup.objects.get(id=data.get("group")) 
        roles = Role.objects.filter(id__in=role_ids)
        
        # Clear old roles and assign new ones
        group.roles.set(roles)
    try:
        group = UserGroup.objects.get(id=data['id'])
        role_categories = RoleCategory.objects.all()
        roles = Role.objects.all() 
        return render(request, "posApp/group_roles.html",{"group":group,"rolecategories":role_categories,"roles":roles})
    except:
        return redirect("groups")
@login_required
def delete_group(request):
    data = request.POST
    resp = {'status': ''}
    try:
        UserGroup.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Group Successfully deleted.')
    except Exception as e:
        resp['msg'] = str(e)
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
# Home page.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total',flat=True))
    context = {
        'page_title':'Home',
        'categories' : categories,
        'products' : products,
        'transaction' : transaction,
        'total_sales' : total_sales,
    }
    return render(request, 'posApp/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'posApp/about.html',context)

#Unit of measurement
@login_required
def uom(request):
    uom_list =Uom.objects.all()
    # category_list = {}
    context = {
        'page_title':'UOM',
        'uom':uom_list,
    }
    return render(request, 'posApp/uom.html',context)
@login_required
def manage_uom(request):
    uom = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            uom = Uom.objects.filter(id=id).first()
    
    context = {
        'uom' : uom
    }
    return render(request, 'posApp/manage_uom.html',context)

@login_required
def save_uom(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_uom = Uom.objects.filter(id = data['id']).update(name=data['name'], shortname=data['shortname'],description = data['description'],)
        else:
            save_uom = Uom(name=data['name'], description = data['description'],shortname=data['shortname'])
            save_uom.save()
        resp['status'] = 'success'
        messages.success(request, 'Uom Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_uom(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Uom.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Uom Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
#Categories
@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
    }
    return render(request, 'posApp/category.html',context)
@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)
@login_required
def low_stock(request):
    low_stock_products = Products.objects.filter(quantity__lt=F('reorder'))
    context = {
        'page_title':'Product List',
        'products':low_stock_products,
    }
    return render(request, 'posApp/products.html',context)
    

@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'categories' : categories,
        'uom':Uom.objects.all()
    }
    return render(request, 'posApp/manage_product.html',context)
def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'posApp/test.html',context)
@login_required
def save_product(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0:
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id=data['category_id']).first()
        uom_id = data.get('uom')  # This will return None if 'uom' is not found
        if uom_id:
            uom = Uom.objects.filter(id=uom_id).first()
        else:
            # Handle the case where 'uom' is missing
            uom = None  # or return an error message, depending on your requirement

        try:
            if 'quantity' in data and data['quantity'].isnumeric():
                quantity = int(data['quantity'])
            else:
                quantity = 0
            if id.isnumeric() and int(id) > 0:
                Products.objects.filter(id=id).update(
                    code=data['code'],
                    category_id=category,
                    name=data['name'],
                    description=data['description'],
                    price=float(data['price']),
                    quantity=quantity,
                    status=data['status'],
                    uom=uom,
                    reorder = data['lowstock']
                )
            else:
                save_product = Products(
                    code=data['code'],
                    category_id=category,
                    name=data['name'],
                    description=data['description'],
                    price=float(data['price']),
                    quantity=quantity,
                    status=data['status'],
                    uom=uom,
                    reorder = data['lowstock']
                )
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except Exception as e:
            resp['msg'] = str(e)
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

#customers
@login_required
def customers(request):
    customer_list = Customer.objects.exclude(default=True)

    context = {
        'page_title':'Customer List',
        'customers':customer_list,
    }
    return render(request, 'posApp/customers.html',context)
@login_required
def manage_customers(request):
    customer = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            customer = Customer.objects.filter(id=id).first()
    
    context = {
        'customer' : customer,
    }
    return render(request, 'posApp/manage_customer.html',context)

@login_required
def save_customer(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    
    if data["name"]=="Walk in Customer":
        resp['msg'] = "You cannot create a customer with this name"
    else:
        try:
            if id.isnumeric() and int(id) > 0:
                Customer.objects.filter(id=id).update(
                    name = data['name'],
                    location = data["location"],
                    phone = data["phone"],
                    email = data["email"],
                )
            else:
                save_customer = Customer(
                    name = data['name'],
                    location = data["location"],
                    phone = data["phone"],
                    email = data["email"]
                )
                save_customer.save()
            resp['status'] = 'success'
            messages.success(request, 'Customer Successfully saved.')
        except Exception as e:
            resp['msg'] = str(e)
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_customer(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Customer.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Customer Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


#suppliers
@login_required
def suppliers(request):
    supplier_list = Supplier.objects.all()
    context = {
        'page_title':'Customer List',
        'suppliers':supplier_list,
    }
    return render(request, 'posApp/suppliers.html',context)
@login_required
def manage_suppliers(request):
    customer = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            customer = Supplier.objects.filter(id=id).first()
    
    context = {
        'customer' : customer,
    }
    return render(request, 'posApp/manage_supplier.html',context)

@login_required
def save_supplier(request):
    data = request.POST
    resp = {'status': 'failed'}
    id = data['id']
    try:
        if id.isnumeric() and int(id) > 0:
            Supplier.objects.filter(id=id).update(
                name = data['name'],
                contact_person = data['contact_person'],
                location = data["location"],
                phone = data["phone"],
                email = data["email"],
            )
        else:
            save_supplier = Supplier(
                name = data['name'],
                location = data["location"],
                phone = data["phone"],
                email = data["email"],
                contact_person = data['contact_person'],
            )
            save_supplier.save()
        resp['status'] = 'success'
        messages.success(request, 'Supplier Successfully saved.')
    except Exception as e:
        resp['msg'] = str(e)
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_supplier(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Supplier.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Supplier Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
#POS
@login_required
def pos(request):
    products = Products.objects.filter(status = 1)
    customer_list = Customer.objects.exclude(default=True)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price)})
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json),
        "customers":customer_list
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'posApp/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status': 'failed', 'msg': ''}
    data = request.POST
    try:
        # Generating a unique code for the sale
        pref = timezone.now().year
        i = 1
        while True:
            code = '{:0>5}'.format(i)
            i += 1
            if not Sales.objects.filter(code=str(pref) + str(code)).exists():
                break
        code = str(pref) + str(code)
        customer = data.get('selectedcustomer')
        customer = get_pos_customer(customer)
        # Creating the sale record
        sale = Sales.objects.create(
            code=code,
            sub_total=data['sub_total'],
            tax=data['tax'],
            tax_amount=data['tax_amount'],
            grand_total=data['grand_total'],
            tendered_amount=data['tendered_amount'],
            amount_change=data['amount_change'],
            customer = customer
        )
        payment_mode = data["payment_mode"]
        if payment_mode == "cash":
            create_cash_payment(sale,data["grand_total"])
        if payment_mode == "mpesa":
            create_mpesa_payment(sale,data["grand_total"])
        if payment_mode == "Null":
            if customer.name != "Walk in Customer":
                createcredit(sale,data["grand_total"],customer)
            else:
                sale.delete()
                resp['msg'] = "Credit sales cannot be made for walk in customers"
                return JsonResponse(resp)
        sale_id = sale.pk
        # Loop through each product in the sale
        for i, prod in enumerate(data.getlist('product_id[]')):
            product_id = prod
            qty = int(data.getlist('qty[]')[i])
            price = float(data.getlist('price[]')[i])

            # Retrieve the product and update its quantity
            product = Products.objects.get(id=product_id)
            if product.quantity < qty:
                resp['msg'] = f"Insufficient stock for product: {product.name}"
                return JsonResponse(resp)

            product.quantity -= qty
            product.save()

            # Create the sales item record
            salesItems.objects.create(
                sale_id = sale,
                product_id = product,
                qty = qty,
                price = price,
                total = qty * price
            )

        # Update response status and sale ID
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        resp['msg'] = "Sale Record has been saved."
        
    except Exception as e:
        resp['msg'] = "An error occurred: " + str(e)

    return JsonResponse(resp)
#Function for creating a credit instance for a sale
def createcredit(sale,amount,customer):
    pref = timezone.now().year
    i = 1
    code=0
    while True:
        code = '{:0>5}'.format(i)
        i += 1
        if not Sales.objects.filter(code=str(pref) + str(code)).exists():
            break
    Credit.objects.create(code = code,sale = sale,amount= amount, customer = customer)
#Function to create a cash payment instance for a sale
def create_cash_payment(sale,amount):
    Cash_Payment.objects.create(amount = amount,sale=sale)
#Function to create a mpesa payment instance for a sale
def create_mpesa_payment(sale,amount):
    Mpesa_Payment.objects.create(amount = amount,sale=sale)
#Fuction to get or create a customer for a sale 
def get_pos_customer(customer):
    if customer.isnumeric() and int(customer) > 0:
        try:
            # Fetch customer by ID
            customer = Customer.objects.get(id=customer)
            return customer
        except Customer.DoesNotExist:
             # Attempt to fetch the first "Walk in Customer" with default=True
            customer = Customer.objects.filter(name="Walk in Customer", default=True).first()

            if not customer:
                # If no "Walk in Customer" exists, create it
                customer= Customer.objects.get_or_create(
                    name="Walk in Customer",
                    defaults={
                        'phone': None,
                        'email': None,
                        'location': None,
                        'default': True,
                    }
                )

            return customer
    else:
        # Attempt to fetch the first "Walk in Customer" with default=True
        if Customer.objects.filter(name="Walk in Customer", default=True).exists():
            customer = Customer.objects.filter(name="Walk in Customer", default=True).first()
            return customer

        else:
            # If no "Walk in Customer" exists, create it
            customer= Customer.objects.create(
                name="Walk in Customer",
                phone= None,
                email=None,
                location= None,
                default= True,
            )
            return customer
#Class for dealing with all sales

class SalesMethods:
    @staticmethod
    def all():
        # Order sales by largest ID first
        sales = Sales.objects.all().order_by("-id")
        sale_data = []

        for sale in sales:
            data = {}
            for field in sale._meta.get_fields(include_parents=False):
                if field.related_model is None:
                    data[field.name] = getattr(sale, field.name)

            # Adding customer and items to the sale data
            data['customer'] = sale.customer
            data['items'] = salesItems.objects.filter(sale_id=sale).all()
            data['item_count'] = len(data['items'])
            data['cash'] = sum([cash.amount for cash in Cash_Payment.objects.filter(sale_id = sale) ])
            data['mpesa'] = sum([mpesa.amount for mpesa in Mpesa_Payment.objects.filter(sale_id = sale) ])
            data['credit'] = sum([credit.amount for credit in Credit.objects.filter(sale_id = sale) ])
            # Format tax_amount if it exists
            if 'tax_amount' in data:
                data['tax_amount'] = format(float(data['tax_amount']), '.2f')

            sale_data.append(data)

        # Get the from_date and to_date based on the sales
        if sales.exists():
            from_date_start = sales.last().date_added.date()  # Earliest date_added
            to_date_end = sales.first().date_added.date()  # Latest date_added
        else:
            from_date_start = None
            to_date_end = None

        context = {
            'page_title': 'Sales Transactions',
            'sale_data': sale_data,
            "from": from_date_start.isoformat() if from_date_start else "",
            "to": to_date_end.isoformat() if to_date_end else "",
             "total_sales":len(sale_data),
            "total_items":sum([sale['item_count'] for sale in sale_data]),
            "total_cash":sum([sale["cash"] for sale in sale_data ]),
            "total_mpesa":sum([sale["mpesa"] for sale in sale_data ]),
            "total_credit":sum([sale["credit"] for sale in sale_data ]),
            "total_amount":sum([sale['grand_total'] for sale in sale_data])

        }
        return context

    @staticmethod
    def dateperiod(from_date, to_date):
        try:
            # Convert the provided dates to datetime objects
            from_date = datetime.strptime(from_date, "%Y-%m-%d")
            to_date = datetime.strptime(to_date, "%Y-%m-%d")

            # Set time to start of the day for from_date
            from_date_start = timezone.make_aware(datetime.combine(from_date, datetime.min.time()))
            # Set time to end of the day for to_date
            to_date_end = timezone.make_aware(datetime.combine(to_date, datetime.max.time()))
        except ValueError:
            # If the date format is incorrect, return an empty list
            return {}

        # Filter sales between the given date range, including time
        sales = Sales.objects.filter(date_added__range=(from_date_start, to_date_end)).order_by("-id")
        sale_data = []

        for sale in sales:
            data = {}
            for field in sale._meta.get_fields(include_parents=False):
                if field.related_model is None:
                    data[field.name] = getattr(sale, field.name)

            # Adding customer and items to the sale data
            data['customer'] = sale.customer
            data['items'] = salesItems.objects.filter(sale_id=sale).all()
            data['item_count'] = len(data['items'])
            data['cash'] = sum([cash.amount for cash in Cash_Payment.objects.filter(sale_id = sale) ])
            data['mpesa'] = sum([mpesa.amount for mpesa in Mpesa_Payment.objects.filter(sale_id = sale) ])
            data['credit'] = sum([credit.amount for credit in Credit.objects.filter(sale_id = sale) ])

            # Format tax_amount if it exists
            if 'tax_amount' in data:
                data['tax_amount'] = format(float(data['tax_amount']), '.2f')

            sale_data.append(data)

        context = {
            'page_title': 'Sales Transactions',
            'sale_data': sale_data,
            "from": from_date.strftime("%Y-%m-%d"),  # Use strftime for proper formatting
            "to": to_date.strftime("%Y-%m-%d"),  # Use strftime for proper formatting
            "total_sales":len(sale_data),
            "total_items":sum([sale['item_count'] for sale in sale_data]),
            "total_cash":sum([sale["cash"] for sale in sale_data ]),
            "total_mpesa":sum([sale["mpesa"] for sale in sale_data ]),
            "total_credit":sum([sale["credit"] for sale in sale_data ]),
            "total_amount":sum([sale['grand_total'] for sale in sale_data])
        }
        return context
    @staticmethod
    def saledetails(id):
        try:
            sale = Sales.objects.get(id = id)
            items = salesItems.objects.filter(sale_id = sale)
            cash_Payments = Cash_Payment.objects.filter(sale = sale)
            mpesa_Payments = Mpesa_Payment.objects.filter(sale = sale)
            credit = Credit.objects.filter(sale = sale)
            context = {
                "sale":sale,
                "items":items,
                "cashpayments":cash_Payments,
                "mpesapayments":mpesa_Payments,
                "credits":credit,
                "itemscount":items.count()
            }
            return context
        except:
            return []
@login_required
def salesList(request):
    sales = SalesMethods()
    context = {}
    if "fromdate" in request.GET and "todate" in request.GET:
        from_date = request.GET.get("fromdate")
        to_date = request.GET.get("todate")
        context = sales.dateperiod(from_date, to_date)
    else:
        context = sales.all()

   
    
    return render(request, 'posApp/sales.html', context)

@login_required
def saledetails(request):
    if "id" in request.GET:
        sales = SalesMethods()
        context = sales.saledetails(request.GET.get('id'))
        if context != []:
            return render(request, 'posApp/saledetails.html',context)
        else:
            return redirect('sales-page')
@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'posApp/receipt.html',context)
@login_required
def invoice(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList,
        "sale":sales
    }

    return render(request, 'posApp/invoice.html',context)
    # return HttpResponse('')

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    if has_role(request, 'Delete sales'):
        try:
            delete = Sales.objects.filter(id = id).delete()
            resp['status'] = 'success'
            messages.success(request, 'Sale Record has been deleted.')
        except:
            resp['msg'] = "An error occured"
            print("Unexpected error:", sys.exc_info()[0])
    else:
        resp['msg'] = "Permission Denied"
    return HttpResponse(json.dumps(resp), content_type='application/json')


def check_product_quantity(request):
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity'))

    try:
        product = Products.objects.get(id=product_id)
        if product.quantity >= quantity:
            response = {
                'status': 'success',
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': product.quantity
                }
            }
        else:
            response = {
                'status': 'failed',
                'msg': f"Insufficient stock for product: {product.name}. Available quantity: {product.quantity}."
            }
    except Products.DoesNotExist:
        response = {
            'status': 'failed',
            'msg': 'Product does not exist.'
        }

    return JsonResponse(response)
#Credit sales
def credit(request):
    credits = Credit.objects.filter(paid = False)
    context = {
        "credits":credits,
        "total":sum(credit.amount for credit in credits)
    }
    return render(request, "posApp/credit.html",context)
@login_required
def paycredit(request):
    resp = {'status':'failed', 'msg':''}
    amount = request.POST.get('amount')
    credit = request.POST.get('id')
    method = request.POST.get('method')

# try:
    credit = Credit.objects.get(id = credit)
    sale = credit.sale
    if method == 'cash':
        Cash_Payment.objects.create(amount = amount,sale = sale)
    else:
        Mpesa_Payment.objects.create(amount = amount,sale = sale)
    credit.amount -= int(amount)
    if credit.amount == 0:
        credit.paid = True
    credit.save()
    resp['status'] = 'success'
    resp['msg'] = 'Successful'
# except:
#     resp['status'] = 'failed'
#     resp['msg'] = 'An error occured'
    return HttpResponse(json.dumps(resp), content_type='application/json')
def todays_transactions_count(request):
    # Get the current date
    today = timezone.now().date()

    # Filter Sales to only include today's transactions
    todays_sales_count = Sales.objects.filter(date_added__date=today).count()

    # Return the count as JSON
    return JsonResponse({'transaction_count': todays_sales_count})
