"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from app.views import (main, category_content, ItemView, cart, create_order,
                       login_view, logout_view, registration)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('category/<name>/', category_content, name='category_content'),
    path('item/<slug:slug>/', ItemView.as_view(), name='show_item'),
    path('cart/', cart, name='cart'),
    path('order/', create_order, name='create_order'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('registration/', registration, name='registration'),
]
