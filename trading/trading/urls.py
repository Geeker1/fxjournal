"""trading URL Configuration

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
from django.contrib.auth.views import LoginView, LogoutView
from journal.views import index, dashboard,\
    forex_detail, binary_detail, forex, binary, stamp
from user.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('option/<str:option>', dashboard, name='dashboard'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('forex/new', forex, name='forex'),
    path('binary/new', binary, name='binary'),
    path('stamp/new', stamp, name='stamp'),
    path('stamp/delete/<uuid:id>', stamp, name='stamp_delete'),
    path('forex/<uuid:id>', forex_detail, name='forex_d'),
    path('binary/<uuid:id>', binary_detail, name='binary_d'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('register', RegisterView.as_view(), name='register'),
]
