# utils.py

from django.contrib.auth.models import User
from Inventory.models import Stock, Brand, Supplier, Product
from transaction.models import Sale,Purchase
from django.db.models import Sum

def get_counts():
    total_products = Stock.objects.aggregate(total_count=Sum('quantity'))
    user_count = User.objects.filter(is_staff=True).count() 
    total_brands = Brand.objects.count()
    total_suppliers = Supplier.objects.count()
    total_product_info = Product.objects.count()
    total_sales = Sale.objects.count() 
    total_purchase = Purchase.objects.count()
    
    return {
        'total_products': total_products['total_count'] if total_products['total_count'] else 0,
        'total_brands': total_brands,
        'total_suppliers': total_suppliers,
        'total_product_info': total_product_info,
        'total_sales': total_sales,
        'total_purchase': total_purchase,
        'user_count': user_count,
    }
