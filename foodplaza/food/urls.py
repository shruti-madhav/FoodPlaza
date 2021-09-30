"""foodplaza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

urlpatterns = [
    path('addfood/', views.addfood),
    path('aboutus/', views.aboutus),
    path('addcustomer/', views.addcustomer),
    path('menu/', views.menu),
    path('allcustomers/', views.allcust),
    path('update/<int:id>', views.update),
    path('updatecustomer/<int:id>', views.updatecust),
    path('delete/<int:id>', views.delete),
    path('deletecustomer/<int:id>', views.deletecust),
    path('home/', views.home),
    path('register/', views.register),
    path('', views.home),
    path('addtocart/', views.addtocart),
    path('showcart/', views.showcart),
    path('updatequantity/', views.updatequantity),
    path('deletecart/<int:id>', views.deletecart),
    path('login/', views.login),
    path('logout/', views.logout),
    path('dologin/', views.dologin),
    path('order/', views.order),
    path('myorder/', views.myorders),
    path('payment/', views.payment),
    path('validate_user', views.validate_user),
    path('changepassword/', views.changepass),
    path('updatepassword/', views.updatepassword),
    path('graph/', views.graph),
    path('graph1/', views.graphone),
    path('graph2/', views.graphtwo),
    path('graph3/', views.graphthree),
    path('graph4/', views.graphfour),
]