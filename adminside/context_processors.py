from .models import Inventory

def low_stock_count(request):
    threshold = 20  # you can change to 30 if needed
    count = Inventory.objects.filter(quantity__lt=threshold).count()
    return {'low_stock_count': count}

def inventory_items_context(request):
    return {
        'inventory_items': Inventory.objects.all()
    }