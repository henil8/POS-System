from django.db import models
from adminside.models import Inventory
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Cart(models.Model):
    Table_id=models.IntegerField()

    def __str__(self):
        return f' Table {self.Table_id}'
    
class cart_items(models.Model):
    Table_id=models.ForeignKey(Cart,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=100)
    quantity=models.IntegerField()
    price=models.IntegerField()

class Orders(models.Model):
    Table_id=models.IntegerField()
    name=models.CharField(max_length=30,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    # def __str__(self):
    #     return f'Table {self.Table_id}'

class order_details(models.Model):
    Table_id=models.ForeignKey(Orders,on_delete=models.CASCADE)
    item_name=models.CharField(max_length=50)
    quantity=models.IntegerField()
    price=models.IntegerField()



class Sales_Report(models.Model):
    item_id=models.IntegerField()
    item_name=models.CharField(max_length=30)
    category=models.CharField(max_length=50)
    quantity=models.IntegerField()
    profit=models.IntegerField()
    timeanddate=models.DateTimeField(null=True)


class Sales_details(models.Model):
    order_id=models.IntegerField()
    cust_name=models.CharField(max_length=50,null=True)
    total_amount=models.IntegerField()
    staff_name=models.CharField()
    payment_method=models.CharField(max_length=20)
    timeanddate=models.DateTimeField(null=True)


class Customer(models.Model):
    name=models.CharField(max_length=100)
    phone_no=PhoneNumberField(null=True)
    email=models.EmailField(null=True)
    timeanddate=models.DateTimeField(auto_now_add=True)