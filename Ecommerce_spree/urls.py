"""Ecommerce_spree URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from cart.views import CartListView , CartItemCreateView , checkout

app_name='Ecommerce_spree'

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("users.urls")),
    path("items/", include("items.urls")),
    path("cart/", CartListView.as_view(),),
    path("cart/add/", CartItemCreateView.as_view() ),
    path("checkout/", checkout.as_view(),),


 
]
