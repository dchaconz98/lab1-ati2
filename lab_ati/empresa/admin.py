from django.contrib import admin

from .models import (
    Empleado, Empresa, SocialMedia
)
# Register your models here.

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "id_tributaria", "servicio_proporciona" )

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido", "ci")

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "valor", "object_id")
