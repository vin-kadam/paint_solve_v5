from django.db import models
from Inventory.models import Product, Supplier,Stock
# Create your models here.
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    purchase_date = models.DateField(auto_now_add=True)
    purchase_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Purchase of {self.product.color_name} from {self.supplier.supplier_name}'

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT ,null=True)
    customer_name = models.CharField(max_length=100)
    customer_phone_no = models.CharField(max_length=15)
    customer_email = models.EmailField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    sale_date = models.DateField(auto_now_add=True)
    sale_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Sale of {self.product.color_name} to {self.customer_name}'
