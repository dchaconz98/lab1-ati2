from django.urls import path
from lab_ati.cliente.views import (
    clientes,
    ver_cliente,
    crear_cliente,
    eliminar_cliente, 
    editar_cliente
    )

urlpatterns = [
    path('<slug:business_id>/clients/', clientes, name='clients'),
    path('<slug:business_id>/clients/create', crear_cliente, name='create-client'),
    path('<slug:business_id>/clients/<slug:id>', ver_cliente, name='detail-client'),
    path('<slug:business_id>/clients/delete/<slug:id>', eliminar_cliente, name='delete-client'),
    path('<slug:business_id>/clients/edit/<slug:id>', editar_cliente, name='edit-client')
]