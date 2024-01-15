from django.shortcuts import render, redirect ,get_object_or_404
from .models import Stock,Supplier,Product,Brand
from Dashboard.utils import get_counts
from django.db import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AddProductForm, AddStockForm   ,StockSearchForm ,BrandForm ,AddSupplierForm,AddStockForm , ProductSearchForm ,SupplierSearchForm
from django.db import IntegrityError




#===============================================product=========================================================
@login_required
def view_product(request):
    form = ProductSearchForm(request.GET)

    products = Product.objects.all()
    counts = get_counts()
    if form.is_valid():
        category = form.cleaned_data.get('category')
        brand = form.cleaned_data.get('brand')
        color_code = form.cleaned_data.get('color_code')

        if category:
            products = products.filter(category__icontains=category)

        if brand:
            products = products.filter(brand__name__icontains=brand)

        if color_code:
            products = products.filter(color_code__icontains=color_code)

    return render(request, 'product/view_product.html', {'products': products, 'form': form,**counts})

@login_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
           
            return redirect('view_product')  
    else:
        form = AddProductForm()
    counts = get_counts()
    return render(request, 'product/add_product.html', {'form': form,**counts})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('view_product')  
    else:
        form = AddProductForm(instance=product)
    counts = get_counts()
    return render(request, 'product/update_product.html', {'form': form,**counts})


@login_required
def delete_product(request, pk):
    delete_products= Product.objects.get(id=pk)
    delete_products.delete()
    delete_products.is_deleted = True
    messages.success(request,"Product Record is deleted Successfully  ")
    return redirect('view_product')


#=========================================================Stock=======================================================================
@login_required
def view_stock(request):
    form = StockSearchForm(request.GET)

    if form.is_valid():
        category = form.cleaned_data.get('category')
        brand = form.cleaned_data.get('brand')
        color_code = form.cleaned_data.get('color_code')

       
        filters = {}
        if category:
            filters['product__category'] = category
        if brand:
            filters['product__brand'] = brand
        if color_code:
            filters['product__color_code__icontains'] = color_code

        stock = Stock.objects.filter(**filters)
    else:
        stock = Stock.objects.all()

    counts = get_counts()
    return render(request, 'Stock/view_Stock.html', {'stock': stock, 'form': form, **counts})

@login_required
def add_Stock(request):
    form = AddStockForm()
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('view_stock')
        else:
            form = AddStockForm()
    counts = get_counts()
    return render(request,'Stock/add_Stock.html',{'form': form,**counts})

@login_required
def update_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = AddStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Record updated successfully!')
            return redirect('view_stock')  
    else:
        form = AddStockForm(instance=stock)
    counts = get_counts()
    return render(request, 'Stock/update_Stock.html', {'form': form,**counts})
@login_required
def delete_stock(request, pk):
    try:
        delete_stock = Stock.objects.get(id=pk)
        delete_stock.delete()
        delete_stock.is_deleted = True
        messages.success(request, "Stock Record is deleted Successfully")
    except Stock.DoesNotExist:
        messages.error(request, "Stock Record does not exist")
    return redirect('view_stock')



#=========================================================Brand=======================================================================
@login_required
def view_brand(request):
    brand = Brand.objects.all()
    counts = get_counts()
    return render(request,'brand/view_brand.html',{'brand':brand,**counts})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand added successfully!')
            return redirect('view_brand')  
    else:
        form = BrandForm()
    counts = get_counts()
    return render(request, 'brand/add_brand.html', {'form': form,**counts})
@login_required
def update_brand(request,pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            messages.success(request, 'Brand Record updated successfully!')
            return redirect('view_brand')  
    else:
        form = BrandForm(instance=brand)
    counts = get_counts()
    return render(request,'brand/update_brand.html',{'form': form,**counts})
@login_required
def delete_brand(request,pk):
    delete_brand= Brand.objects.get(id=pk)
    delete_brand.delete()
    delete_brand.is_deleted = True
    messages.success(request,"Brand Record is deleted Successfully  ")
    return redirect('view_brand')


#===========================================================suppplier==================================================================== 
@login_required
def view_supplier(request):
    if request.method == 'GET':
        form = SupplierSearchForm(request.GET)
        if form.is_valid():
            supplier_name = form.cleaned_data.get('supplier_name', '')
            supplier_email = form.cleaned_data.get('supplier_email', '')

            # Filter suppliers based on form input
            suppliers = Supplier.objects.filter(
                supplier_name__icontains=supplier_name,
                supplier_email__icontains=supplier_email,
            )

            counts = get_counts()
            return render(request, 'supplier/view_supplier.html', {'supplier': suppliers, 'form': form, **counts})

    else:
        form = SupplierSearchForm()

    supplier = Supplier.objects.all()
    counts = get_counts()
    return render(request, 'supplier/view_supplier.html', {'supplier': supplier, 'form': form, **counts})

#add_supplier
@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = AddSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier added successfully!')
            return redirect('view_supplier')  # Redirect to supplier list page
    else:
        form = AddSupplierForm()
    counts = get_counts()
    return render(request, 'supplier/add_supplier.html', {'form': form,**counts})


@login_required
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = AddSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supplier Record is updated successfully!')
            return redirect('view_supplier')  
    else:
        form = AddSupplierForm(instance=supplier)
    counts = get_counts()
    return render(request, 'supplier/update_supplier.html', {'form': form,**counts})


@login_required
def delete_supplier(request, pk):
    delete_it = Supplier.objects.get(id=pk)
    delete_it.delete()
    delete_it.is_deleted = True
    messages.success(request,"Supplier Record is deleted Successfully  ")
    return redirect('view_supplier')
