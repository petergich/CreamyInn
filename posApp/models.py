from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Create your models here.

# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True) 
#     firstname = models.TextField() 
#     middlename = models.TextField(blank=True,null= True) 
#     lastname = models.TextField() 
#     gender = models.TextField(blank=True,null= True) 
#     dob = models.DateField(blank=True,null= True) 
#     contact = models.TextField() 
#     address = models.TextField() 
#     email = models.TextField() 
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE) 
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE) 
#     date_hired = models.DateField() 
#     salary = models.FloatField(default=0) 
#     status = models.IntegerField() 
#     date_added = models.DateTimeField(default=timezone.now) 
#     date_updated = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '
class Customer(models.Model):
    name = models.CharField(max_length = 150)
    phone = models.CharField(max_length = 50,null=True,default=None)
    email = models.CharField(max_length = 150,null=True,default=None)
    location = models.CharField(max_length = 150,null=True,default=None)
    default=models.BooleanField(default=False)
class Supplier(models.Model):
    name = models.CharField(max_length = 150)
    contact_person = models.CharField(max_length = 150)
    phone = models.CharField(max_length = 50,null=True,default=None)
    email = models.CharField(max_length = 150,null=True,default=None)
    location = models.CharField(max_length = 150,null=True,default=None)
class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Uom(models.Model):
    name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    def __str__ (self):
        return self.name
class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.FloatField(default=0)
    reorder = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)  # New quantity field
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    uom= models.ForeignKey(Uom,default=None,null=True,on_delete=models.SET_NULL)
    def __str__(self):
        return self.code + " - " + self.name
   
class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    customer= models.ForeignKey(Customer,default=None,on_delete=models.SET_NULL,null=True)
    cash = models.CharField(max_length=100, blank=True, null=True)  # New field for cash payments
    mpesa = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.code
class Mpesa_Payment(models.Model):
    sale = models.ForeignKey(Sales,on_delete=models.CASCADE)
    code = models.CharField(max_length=254,null=True)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
class Cash_Payment(models.Model):
    sale = models.ForeignKey(Sales,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
class Credit(models.Model):
    code = models.CharField(max_length = 20,default = None,null=True)
    sale = models.ForeignKey(Sales,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default = 0)
    paid = models.BooleanField(default = False)
    customer= models.ForeignKey(Customer,on_delete=models.CASCADE)
class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
class RoleCategory(models.Model):
    name = models.CharField(max_length = 254)
class Role(models.Model):
    name = models.CharField(max_length = 254)
    description = models.CharField(max_length= 1000)
    category = models.ForeignKey(RoleCategory,on_delete=models.CASCADE)
class UserGroup(models.Model):
    name = models.CharField(max_length = 254)
    description = models.CharField(max_length = 1000,default=None,null=True)
    roles = models.ManyToManyField(Role)
class CustomUser(AbstractUser):
    group = models.ForeignKey(UserGroup, default=None,on_delete = models.SET_NULL,null=True,)
    name = models.CharField(max_length = 254)
    roles = models.ManyToManyField(Role, related_name='users', blank=True)
    phone = models.CharField(max_length = 50)
    plainpassword = models.CharField(max_length = 254,default="null") 
    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

    def has_group(self, group_name):
        return self.groups.filter(name=group_name).exists()



