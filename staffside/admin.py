from django.contrib import admin
from .models import cart_items,Cart,order_details,Orders,Sales_Report,Sales_details


# Register your models here.
class CartAdmin(admin.ModelAdmin):
  list_display = ("id", "Table_id")
  
admin.site.register(Cart, CartAdmin)


class cart_itemsAdmin(admin.ModelAdmin):
  list_display = ("Table_id","item_name","quantity","price")
  
admin.site.register(cart_items, cart_itemsAdmin)


class OrderAdmin(admin.ModelAdmin):
  list_display = ("id", "Table_id","name")
  
admin.site.register(Orders, OrderAdmin)


class order_detailsAdmin(admin.ModelAdmin):
  list_display = ("Table_id","item_name","quantity","price")
  
admin.site.register(order_details, order_detailsAdmin)

class Sales_ReportAdmin(admin.ModelAdmin):
  list_display = ("item_id","item_name","category","quantity","profit","timeanddate")
  
admin.site.register(Sales_Report, Sales_ReportAdmin)

class Sales_detailsAdmin(admin.ModelAdmin):
  list_display = ("order_id","cust_name","total_amount","staff_name","payment_method","timeanddate")
  
admin.site.register(Sales_details, Sales_detailsAdmin)