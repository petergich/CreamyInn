from django.contrib import admin
from posApp.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(salesItems)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CustomUser)
admin.site.register(Credit)
admin.site.register(Mpesa_Payment)
admin.site.register(Cash_Payment)

# admin.site.register(Employees)
