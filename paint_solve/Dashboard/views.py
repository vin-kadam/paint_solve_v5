from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from Inventory.models import Stock ,Brand,Supplier,Product
from transaction.models import Sale
from transaction.models import Sale , Purchase
from django.http import JsonResponse
from Dashboard.utils import get_counts

# Create your views here.
def get_dashboard_data():
    category_counts = Product.objects.values('category').annotate(total=Count('category'))

    # Get stock quantities for each product
    stock_data = Stock.objects.select_related('product').values_list('product__color_name', 'quantity')

    brand_counts = []
    brands = Brand.objects.all()
    for brand in brands:
        total = brand.product_set.count() 
        brand_counts.append({'name': brand.name, 'total': total})

    # Count of sales by product
    sales_counts = []
    products = Product.objects.all()
    for product in products:
        total_sales = Sale.objects.filter(product=product).count() 
        sales_counts.append({'product': product, 'total': total_sales})

    return {
        'category_counts': category_counts,
        'stock_data': stock_data,
        'brand_counts': brand_counts,
        'sales_counts': sales_counts,
    }
@login_required()
def home(request):
    counts = get_counts()
    context = get_dashboard_data()
    return render(request, 'home.html', {**context, **counts})
def sold_products_by_category(request):
   
    category_sales = Sale.objects.values('product__category').annotate(count=Count('id'))

   
    categories = []
    counts = []
    for category_sale in category_sales:
        categories.append(category_sale['product__category'])
        counts.append(category_sale['count'])

    data = {
        'categories': categories,
        'counts': counts,
    }
    return JsonResponse(data)