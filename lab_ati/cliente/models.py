from django.db import models
from lab_ati.empresa.models import DirABC
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ClientType(models.TextChoices):
    LABORA_EMPRESA = 'LE', _('Labora empresa')
    STUDENT = 'SO', _('Estudiante')
    OTHER = 'JR', _('Otro')

class Cliente(DirABC):

    nombre = models.TextField(_("Nombre y Apellido"))
    tipo = models.TextField(
        choices=ClientType.choices,
    )
    empcompany=models.TextField(_("Compañia/Organismo"))
    cargo=models.TextField(_("Cargo"))
    empresa=models.ForeignKey(
        to="empresa.Empresa",
        on_delete=models.CASCADE,
        related_name="clientes",
        verbose_name=_("Empresa"),
        null=True,
        blank=True,
    )
    personal_email=models.TextField(_("Email personal"))
    tlf_celular=models.TextField(_("Teléfono celular"))
    whatsapp=models.TextField(_("Whatsapp"))
    servicio_ofrecido = models.TextField(_("Servicio ofrecido"))
    curso_interes=models.TextField(_("Curso de interés"))
    frecuencia=models.TextField(_("Frecuencia con la que desea mantenerse informado"))

    def __str__(self):
        return f"{self.nombre} {self.tipo}"
