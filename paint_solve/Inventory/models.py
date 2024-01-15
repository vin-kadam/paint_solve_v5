# models.py
from django.db import models
from django.db.models.signals import Signal
from django.dispatch import receiver

from django.core.validators import RegexValidator



class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, help_text="Description of the paint brand")
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True, help_text="Logo of the paint brand")
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = (
    ('Oil Paint', 'Oil Paint'),
    ('Cement Paint', 'Cement Paint'),
    ('Distemper Paint', 'Distemper Paint'),
    ('Emulsion Paint', 'Emulsion Paint'),
    ('Whitewash', 'Whitewash'),
    ('Enamel Paint', 'Enamel Paint'),
    ('Acrylic Emulsion Paint', 'Acrylic Emulsion Paint'),
    ('Bituminous Paint', 'Bituminous Paint'),
    ('Synthetic Rubber Paint', 'Synthetic Rubber Paint'),
    ('Anti-Corrosion Paint', 'Anti-Corrosion Paint'),
    )

    color_name = models.CharField(max_length=100, null=False)
    category =models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT ,null=True)
    color_code = models.CharField(
        max_length=10,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^#[0-9A-Fa-f]{6}$',  # Matches # followed by 6 characters in 0-9, A-F, or a-f
                message='Color code must start with "#" and have exactly 6 characters following it.',
            ),
        ],
    )
    def __str__(self):
        return self.color_name

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,null=True)
    quantity = models.PositiveIntegerField(null=False, default=0)
    price = models.PositiveIntegerField(null=False)
    alert_threshold = models.IntegerField(default=10, help_text="Set the alert threshold for low stock")

    def __str__(self):
        return f'{self.product.color_name}'

    def check_quantity_threshold(self):
        if self.quantity <= self.alert_threshold:
            stock_alert.send(sender=self.__class__, product=self)

# Signal
stock_alert = Signal()

# Signal handler
@receiver(stock_alert)
def stock_alert_handler(sender, **kwargs):
    product = kwargs['product']
    
    
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    supplier_phone_no = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{10,15}$',
                message='Phone number must be between 10 and 15 digits.'
            ),
        ],
    )
    supplier_email = models.EmailField()
    supplied_products = models.ManyToManyField(Product,related_name='suppliers')

    def __str__(self):
        return self.supplier_name
