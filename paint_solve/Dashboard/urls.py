from django.urls import path 

from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('sold-products-by-category/', views.sold_products_by_category, name='sold_products_by_category'),
    
    

    
]
