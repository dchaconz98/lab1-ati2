from django.db import models
from lab_ati.empresa.models import EmpresaABC
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core import validators

# Create your models here.

class Proveedor(EmpresaABC):
    email_regex = '^[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$'
    tlf_regex = '^\+?([0-9]{1,3}|[1]\-?[0-9]{3})?\-?([0-9]{1,4})\-?([0-9]{3}\-?[0-9]{2}\-?[0-9]{2})$'
    
    #tlf=models.TextField(_("Teléfono del proveedor"))
    representante=models.TextField(_("Nombre del representante"))
    cargo=models.TextField(_("Cargo del representante"))
    #email_representante=models.EmailField(_("Correo del representante"))
    email_personal_representante=models.EmailField(_("Correo personal del representante"))
    tlf_representate=models.TextField(_("Teléfono celular del representante"))
    tlf_local=models.TextField(_("Teléfono local del representante"))
    pais_representante=models.TextField(_("Pais de residencia de representante"))
    empresa=models.ForeignKey(
        to="empresa.Empresa",
        on_delete=models.CASCADE,
        related_name="proveedores",
        null=True,
        blank=True,
        verbose_name=_("Empresa"),
    )

    tlf=models.TextField(
        _("Teléfono del proveedor"),
        validators=[validators.RegexValidator(
            regex=tlf_regex,
            message=_('El campo debe ser un número de teléfono'),
            code='tlf_invalido'
        )],
    )

    email_representante=models.EmailField(
        _("Email"),
        validators=[validators.RegexValidator(
            regex=email_regex,
            message=_('El campo debe ser un correo valido'),
            code='correo_invalido'
        )]                      
    )


    @property
    def redes_representante(self):
        return self.redes_sociales.filter(belongs_to='redes_representante')

    @property
    def redes_proveedor(self):
        return self.redes_sociales.filter(belongs_to='redes_proveedor')
