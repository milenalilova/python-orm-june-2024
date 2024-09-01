import os
from itertools import product

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Count, Q, F
from main_app.models import Profile, Product, Order


# Create queries within functions

def get_profiles(search_string=None):
    if search_string is None:
        return ""

    profiles = (Profile.objects.annotate(order_count=Count('orders')).
                filter(Q(full_name__icontains=search_string)
                       | Q(email__icontains=search_string)
                       | Q(phone_number__icontains=search_string))).order_by('full_name')

    if not profiles:
        return ""

    result = []
    for p in profiles:
        result.append(
            f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_count}")

    return '\n'.join(result)


def get_loyal_profiles():
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ""

    result = []
    for p in profiles:
        result.append(f"Profile: {p.full_name}, orders: {p.order_numbers}")

    return '\n'.join(result)


def get_last_sold_products():
    try:
        last_order = Order.objects.prefetch_related('products').latest('creation_date')
        last_products = last_order.products.all().order_by('name')

        if last_products:
            result = [p.name for p in last_products]
            return f"Last sold products: {', '.join(result)}"
        return ""

    except Order.DoesNotExist:
        return ""


def get_top_products():
    products = Product.objects.annotate(orders_count=Count('product_orders')).filter(orders_count__gt=0).order_by('-orders_count', 'name')[:5]

    # top_products = Product.objects.annotate(num_orders=Count('orders')).filter(num_orders__gt=0).order_by('-num_orders', 'name')[:5]

    if not products:
        return ""

    result = []
    for p in products:
        result.append(f"{p.name}, sold {p.orders_count} times")
    products_str = '\n'.join(result)

    return f"Top products:\n{products_str}"


def apply_discounts():
    orders = Order.objects.annotate(products_count=Count('products')).filter(products_count__gt=2).filter(
        is_completed=False).update(total_price=F('total_price') * 0.9)

    return f"Discount applied to {orders} orders."


def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not order:
        return ""

    order.is_completed = True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()

    return f"Order has been completed!"
