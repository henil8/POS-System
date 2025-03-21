from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Inventory,Branch,Purchase,CustomUser,Categories

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
  list_display = ("id", "location", "area","manager_id","phone_no","status")
  
admin.site.register(Branch, BranchAdmin)


class PurchaseAdmin(admin.ModelAdmin):
  list_display = ("food_item_id", "food_item", "cost_price","supplier_id","purchased_date","payment_status")
  
admin.site.register(Purchase, PurchaseAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ( "id","image", "food_item_name","category","description","quantity","sell_price","cost_price","mfg_date","exp_date")
  
admin.site.register(Inventory, InventoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ("id", "category_name", "status")
  
admin.site.register(Categories, CategoryAdmin)


class CustomUserAdmin(UserAdmin):   
   add_form=UserCreationForm
   form=UserChangeForm
   model=CustomUser
   list_display=['id','email','username','first_name','last_name']
   add_fieldsets=UserAdmin.add_fieldsets + (
     (None,{'fields':('email','first_name','last_name','role','branch','phone_no','image')}),
    )
   fieldsets = UserAdmin.fieldsets +  (
      (None,{'fields':('role','branch','phone_no','image')}),
    )
   

admin.site.register(CustomUser,CustomUserAdmin)