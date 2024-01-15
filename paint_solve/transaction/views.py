from django.shortcuts import render, redirect
from .forms import SaleForm, PurchaseForm
from .models import Sale, Purchase, Stock
from django.contrib import messages
from Dashboard.utils import get_counts
def view_purchase_transaction(request):
    purchases = Purchase.objects.all()
    counts = get_counts()
    return render(request,'purchase/view_purchase.html',{'purchases':purchases,**counts})
def view_sale_transaction(request):
    sales = Sale.objects.all()
    counts = get_counts()
    return render(request,'sales/view_sales.html',{'sales':sales,**counts})
def purchase_transaction(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.save()

            product = purchase.product
            stock, created = Stock.objects.get_or_create(product=product)
            stock.quantity += purchase.quantity
            stock.save()
            messages.success(request, 'Purchase transaction successful!')
            return redirect('view_purchase')  
    else:
        form = PurchaseForm()
    counts = get_counts()
    return render(request, 'purchase/purchase_transaction.html', {'form': form,**counts})

def sale_transaction(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.save()

            product = sale.product
            stock, created = Stock.objects.get_or_create(product=product)
            stock.quantity -= sale.quantity
            stock.save()
            messages.success(request, 'Sales transaction completed!')
            return redirect('view_sales')  # Redirect to a success URL
    else:
        form = SaleForm()
    counts = get_counts()
    return render(request, 'sales/sale_transaction.html', {'form': form,**counts})

