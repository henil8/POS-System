from django import template

register = template.Library()

@register.filter(name='low_stock')
def low_stock(items, threshold):
    return [item for item in items if item.quantity < threshold]