
from django.urls import path 
from . import views


urlpatterns = [
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('register/',views.register_user,name="register"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('view_user/',views.view_user,name="view_user"),
   path('modify_user/<int:pk>/', views.modify_user, name='modify_user'),
   path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    
]
