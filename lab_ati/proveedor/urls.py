from django.urls import path
from . import views

urlpatterns = [
  path('', views.listProveedor, name='listProveedor'),
  path('ver', views.seeProveedor, name='seeProveedor'),
  path('crear', views.createProveedor, name='createProveedor'), 
  path('modificar', views.updateProveedor, name='updateProveedor'), 
  path('eliminar', views.deleteProveedor, name='deleteProveedor') 
]