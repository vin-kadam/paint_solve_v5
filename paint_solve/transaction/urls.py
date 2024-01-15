from django.urls import path
from . import views
urlpatterns = [



    path('sales/',views.sale_transaction,name="sales"),
    path('purchase/',views.purchase_transaction,name="purchase"),
    path('view_purchase/',views.view_purchase_transaction,name="view_purchase"),
    path('view_sales/',views.view_sale_transaction,name="view_sales"),
    
    


]
