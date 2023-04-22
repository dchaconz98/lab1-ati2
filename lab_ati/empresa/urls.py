from django.urls import path
from . import views

app_name = "empresa"

urlpatterns = [
    path("", views.BusinessListView.as_view(), name="business-list"),
    path("create", views.CreateBusinessView.as_view(), name="create-business"),
    path("details/<slug:pk>", views.BusinessDetailsView.as_view(), name="business-details"),
    path("edit/<slug:pk>", views.EditBusinessView.as_view(), name="edit-business"),
    path("delete/<slug:pk>", views.DeleteBusinessView.as_view(), name="delete-business"),
    path("<slug:business_id>/employees/create", views.CreateEmployeeView.as_view(), name="create-employee"),
    path("<slug:business_id>/employees/edit/<slug:pk>", views.EditEmployeeView.as_view(), name="edit-employee"),
    path("<slug:business_id>/employees/", views.ListEmployeeView.as_view(), name="list-employee"),
    path("<slug:business_id>/employees/delete/<slug:pk>", views.DeleteEmployeeView.as_view(), name="delete-employee"),
    path("<slug:business_id>/employees/<slug:pk>", views.DetailEmployeeView.as_view(), name="detail-employee"),
    path("guardar-logo/<slug:business_id>", views.actualizar_logo_empresa, name="update-logo-employee"),
]
