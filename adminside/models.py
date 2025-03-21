from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import authenticate
from django.contrib.auth.models import User,AbstractUser,Group,Permission
from django.utils.timezone import now

class Branch(models.Model):
    status=[
        ('Open',"Open"),
        ('Close',"Close")
        ]
    id=models.AutoField(primary_key=True)
    location=models.CharField(max_length=50)
    area=models.CharField(max_length=50)
    manager_id=models.IntegerField(null=False)
    phone_no=PhoneNumberField()
    status=models.CharField(max_length=10,choices=status)

    def __str__(self):
        return f"{self.location}-{self.area}"

class Purchase(models.Model):
    food_item_id=models.IntegerField(primary_key=True)
    food_item=models.CharField(max_length=50)
    cost_price=models.IntegerField(null=False)
    supplier_id=models.IntegerField(null=False)
    purchased_date=models.DateField()
    payment_status=models.CharField(max_length=10)



class Categories(models.Model):
  status=[
        ('Available',"Available"),
        ('Not Available',"Not Available")
        ]
  id = models.AutoField(primary_key=True)
  category_name = models.CharField(max_length=50)
  status= models.CharField(max_length=20,choices=status)

  def __str__(self):
      return f'{self.category_name}'

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)  
    image=models.ImageField(blank=True,upload_to='food_items/')
    food_item_name=models.CharField(max_length=100)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    description=models.TextField(max_length=100,null=True)
    quantity=models.IntegerField(null=True)
    sell_price=models.IntegerField(null=False)
    cost_price=models.IntegerField(null=False)
    mfg_date=models.DateField()
    exp_date=models.DateField()

    def __str__(self):
      return self.food_item_name

class CustomUser(AbstractUser):
     groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # ✅ Renaming the reverse relation
        blank=True
    )
     user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # ✅ Renaming the reverse relation
        blank=True
    )
     role=models.CharField(max_length=30)
     branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
     phone_no=PhoneNumberField(null=True,blank=True)
     image=models.ImageField(height_field=None,width_field=None,upload_to=None,blank=True,null=True)
     
     