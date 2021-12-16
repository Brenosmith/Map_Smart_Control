"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "main"

urlpatterns = (
    path("", views.homepage, name="homepage"),
    path("register", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("add_status", views.add_status, name="add_status"),
    path("add_equipment", views.add_equipment, name="add_equipment"),
    path("account", views.dashboard, name='dashboard'),
    path("pivot_data", views.pivot_data, name='pivot_data'),
    path("pivot_data2", views.pivot_data2, name='pivot_data2'),
    path("<single_slug>", views.single_slug_request, name="single_slug"),
)
