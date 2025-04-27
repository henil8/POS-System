from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import Inventory,Branch,CustomUser,Categories,Tables,Purchase,Supplier

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
  list_display = ("id", "location", "area","manager_id","phone_no","status")
  
admin.site.register(Branch, BranchAdmin)


class PurchaseAdmin(admin.ModelAdmin):
  list_display = ( "id","food_item","quantity", "cost_price","supplier_company_Person","phone_no","purchased_date","payment_status")
  
admin.site.register(Purchase, PurchaseAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ( "id","image", "food_item_name","category","description","quantity","sell_price","cost_price","mfg_date","exp_date")
  
admin.site.register(Inventory, InventoryAdmin)

class SupplierAdmin(admin.ModelAdmin):
  list_display = ( "supplier_name","company_name", "supplier_email","supplier_phone","address","branch")
  
admin.site.register(Supplier, SupplierAdmin)

class CategoryAdmin(admin.ModelAdmin):
  list_display = ("id", "category_name", "status")
  
admin.site.register(Categories, CategoryAdmin)

class TablesAdmin(admin.ModelAdmin):
  list_display = ("id", "table_id","seats", "status")
  
admin.site.register(Tables, TablesAdmin)

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