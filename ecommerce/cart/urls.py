"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cart import views
app_name='cart'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('addtocart/<int:pk>/',views.addtocart,name='addtocart'),
    path('cartview',views.cartview,name='cartview'),
    path('cartdecrement/<int:pk>/',views.cart_decrement,name='cartdecrement'),
    path('cartremove/<int:pk>/',views.cart_remove,name='cartremove'),
    path('placeorder',views.orderform,name='placeorder'),
    path('status/<u>',views.payment_status,name='payment_status'),
    path('orderview',views.orderview,name='orderview'),



]
