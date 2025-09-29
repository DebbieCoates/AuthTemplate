from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
        # Authentication URLs
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_password/', views.update_password, name='update_password'),
    
    #Customer
    path('customers/', views.Customers, name='customers'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('customer_add/', views.customer_add, name='customer_add'),
    path('customer_edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('customer_delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    ]