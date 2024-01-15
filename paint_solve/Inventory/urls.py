from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #stock urls
    path('view_stock/',views.view_stock,name="view_stock"),
    path('add_Stock/',views.add_Stock,name="add_Stock"),
    path('delete_Stock/<int:pk>',views.delete_stock,name="update_Stock"),
    path('update_Stock/<int:pk>',views.update_stock,name="update_Stock"),
    
    #Product urls
    path('add_product/', views.add_product, name='add_product'),    
    path('view_product/', views.view_product, name='view_product'),    
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'), 
    
    #brand Urls
    path('add_brand',views.add_brand,name="add_brand"),
    path('view_brand',views.view_brand,name="view_brand"),
    path('update_brand/<int:pk>',views.update_brand,name="update_brand"),
    path('delete_brand/<int:pk>',views.delete_brand,name="delete_brand"),
    
    #supplier urls 
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('update_supplier/<int:pk>', views.update_supplier, name='update_supplier'),
    path('delete_supplier/<int:pk>/', views.delete_supplier, name='delete_supplier'),
    path('view_supplier/', views.view_supplier, name='view_supplier'),
    
    
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)