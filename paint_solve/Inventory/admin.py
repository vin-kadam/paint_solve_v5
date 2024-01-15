from django.contrib import admin
from .models import Stock ,Product ,Brand,Supplier
from django.contrib.auth.models import Group

# Register your models here.
admin.site.register(Stock)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Supplier)