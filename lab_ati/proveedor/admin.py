from django.contrib import admin

from .models import (
    Proveedor
)

# Register your models here.
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre","representante", "email")
