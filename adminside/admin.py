from django.contrib import admin
from .models import Inventory,Branch,Purchase

# Register your models here.
class BranchAdmin(admin.ModelAdmin):
  list_display = ("id", "location", "area","manager_id","phone_no","status")
  
admin.site.register(Branch, BranchAdmin)


class PurchaseAdmin(admin.ModelAdmin):
  list_display = ("food_item_id", "food_item", "cost_price","supplier_id","purchased_date","payment_status")
  
admin.site.register(Purchase, PurchaseAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ("food_item_id", "image", "food_item_name","category","description","quantity","branch","sell_price","cost_price","mfg_date","exp_date")
  
admin.site.register(Inventory, InventoryAdmin)


