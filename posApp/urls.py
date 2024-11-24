from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('test', views.test, name="test-page"),
    #Authentications
    path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    #Categories
    path('category', views.category, name="category-page"),
    path('manage_category', views.manage_category, name="manage_category-page"),
    path('save_category', views.save_category, name="save-category-page"),
    path('delete_category', views.delete_category, name="delete-category"),
    #UOM
    path('uom', views.uom, name="uom"),
    path('manage_uom', views.manage_uom, name="manage_uom-page"),
    path('saveuom', views.save_uom, name="save_uom-page"),
    path('deleteuom', views.delete_uom, name="delete-uom"),
    #Products
    path('products', views.products, name="product-page"),
    path('manage_products', views.manage_products, name="manage_products-page"),
    path('save_product', views.save_product, name="save-product-page"),
    path('delete_product', views.delete_product, name="delete-product"),
    path('lowstock',views.low_stock,name="lowstock"),
    path('check_product_quantity/', views.check_product_quantity, name='check_product_quantity'),
    #POS
    path('pos', views.pos, name="pos-page"),
    path('checkout-modal', views.checkout_modal, name="checkout-modal"),
    path('save-pos', views.save_pos, name="save-pos"),
    path('receipt', views.receipt, name="receipt-modal"),
    path('invoice',views.invoice,name='invoice-modal'),
    path('todays-transactions-count/', views.todays_transactions_count, name='todays-transactions-count'),
    #customers
    path('customers', views.customers, name="customer-page"),
    path('manage_customers', views.manage_customers, name="manage_customers-page"),
    path('save_customer', views.save_customer, name="save-customer-page"),
    path('delete_customer', views.delete_customer, name="delete-customer"),
    #suppliers
    path('suppliers', views.suppliers, name="supplier-page"),
    path('manage_suppliers', views.manage_suppliers, name="manage_supplier-page"),
    path('save_supplier', views.save_supplier, name="save-supplier-page"),
    path('delete_supplier', views.delete_supplier, name="delete-supplier"),
    #users
    path("users",views.users,name="users"),
    path("manage_users-page",views.manage_users,name="manage_users-page"),
    path("delete-user",views.delete_user,name="delete-user"),
    path('save_user', views.save_user, name="save_user-page"),
    path('user_roles',views.user_roles,name="user_roles"),
    # User groups
    path("groups",views.groups,name="groups"),
    path("manage_groups-page",views.manage_groups,name="manage_groups-page"),
    path("delete-group",views.delete_group,name="delete-group"),
    path('save_group', views.save_group, name="save_group-page"),
    path('group_roles',views.group_roles,name="group_roles"),
    #sales
    path('credits',views.credit,name="credits"),
    path('sales', views.salesList, name="sales-page"),
    path('delete_sale', views.delete_sale, name="delete-sale"),
    path('saledetails',views.saledetails, name= "saledetails"),
    path('paycredit',views.paycredit,name="paycredit")
]