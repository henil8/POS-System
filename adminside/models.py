from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Branch(models.Model):
    id=models.IntegerField(primary_key=True)
    location=models.CharField(max_length=50)
    area=models.CharField(max_length=50)
    manager_id=models.IntegerField(null=False)
    phone_no=PhoneNumberField()
    status=models.CharField(max_length=10)

class Purchase(models.Model):
    food_item_id=models.IntegerField(primary_key=True)
    food_item=models.CharField(max_length=50)
    cost_price=models.IntegerField(null=False)
    supplier_id=models.IntegerField(null=False)
    purchased_date=models.DateField()
    payment_status=models.CharField(max_length=10)

class Inventory(models.Model):
    food_item_id=models.IntegerField(primary_key=True)
    image=models.ImageField(blank=True)
    food_item_name=models.CharField(max_length=20)
    category=models.CharField(max_length=20)
    description=models.TextField(max_length=100)
    quantity=models.IntegerField(null=True)
    branch=models.CharField(max_length=20)
    sell_price=models.IntegerField(null=False)
    cost_price=models.IntegerField(null=False)
    mfg_date=models.DateField()
    exp_date=models.DateField()