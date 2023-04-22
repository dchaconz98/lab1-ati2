import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import validators

# Create your models here.
class DirABC(models.Model):

    ciudad = models.TextField(_("Ciudad"))
    pais = models.TextField(_("Pais"))
    redes_sociales = GenericRelation(
        to="empresa.SocialMedia",
        related_query_name="redes_sociales"
    )

    class Meta:
        abstract = True

class EmpresaABC(DirABC):
    email_regex = '^[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nombre = models.TextField(_("Nombre"))
    id_tributaria = models.TextField(_("Número de identificación tributaria"))
    email = models.EmailField(
        _("Email"),
        validators=[validators.RegexValidator(
            regex=email_regex,
            message=_('El campo debe ser un correo valido'),
            code='correo_invalido'
        )]                      
    )
    direccion = models.TextField(_("Dirección"))
    web_site = models.URLField(_("Sitio web"))
    servicio_proporciona = models.TextField(_("Servicio que proporciona"))
    logo = models.FileField(upload_to="images/logos", default="logo.png")


    def __str__(self):
        return f"{self.nombre} {self.id_tributaria}"

    class Meta:
        abstract = True

class Empresa(EmpresaABC):
    tlf_regex = '^\+?([0-9]{1,3}|[1]\-?[0-9]{3})?\-?([0-9]{1,4})\-?([0-9]{3}\-?[0-9]{2}\-?[0-9]{2})$'

    servicio_ofrecido = models.TextField(_("Servicio que le ofrecimos"))
    servicio_proporciona = models.TextField(_("Servicio que proporciona"))
    whatsapp=models.TextField(
        _("Whatsapp"),
        validators=[validators.RegexValidator(
            regex=tlf_regex,
            message=_('El campo debe ser un número de teléfono'),
            code='tlf_whatsapp_invalido'
        )]
    )
    telefono=models.TextField(_("Teléfono"),
        validators=[validators.RegexValidator(
            regex=tlf_regex,
            message=_('El campo debe ser un número de teléfono'),
            code='tlf_invalido'
        )]
    )
    curso_interes=models.TextField(_("Curso de interés"))
    frecuencia=models.TextField(_("Frecuencia con la que desea mantenerse informado"))
    cliente_empresa = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Cliente de empresa"),
        related_name="clientes_empresa",
    )

# Generic Model
class SocialMedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.TextField()
    valor = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    # A hack to allow models have "multiple" social_media fields
    belongs_to = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    def __str__(self):
        return f"{self.nombre} {self.valor}"

class Empleado(DirABC):

    tlf_regex = '^\+?([0-9]{1,3}|[1]\-?[0-9]{3})?\-?([0-9]{1,4})\-?([0-9]{3}\-?[0-9]{2}\-?[0-9]{2})$'
    ci_regex = '^(([a-zA-Z]{3}|[a-zA-Z]-)[0-9]{1,3}\.?[0-9]{1,3}\.?[0-9]{1,3})$|^([0-9A-Z]{10})$'

    class Modalidad(models.TextChoices):
        FIJO='FIJO', _('Fijo')
        HONORARIO_PROFESIONALES='HP', _('Honorario profesionales')

    nombre = models.TextField(_("Nombre"))
    apellido = models.TextField(_("Apellido"))
    ci = models.TextField(_("Cédula o nro pasaporte"), validators=[validators.RegexValidator(
                                    regex=ci_regex,
                                    message=_('El campo debe ser una cédula de identidad o número de pasaporte'),
                                    code='ci_invalido'
                                )
                            ])
    cargo=models.TextField(_("Cargo"))

    empresa=models.ForeignKey(
        to="empresa.Empresa",
        on_delete=models.CASCADE,
        related_name="empleados",
        verbose_name=_("Empresa"),
        null=True,
        blank=False,
    )
    modalidad_contratacion=models.TextField(
        verbose_name=_("Modalidad de contratación"),
        choices=Modalidad.choices
    )
    email_emp = models.EmailField(_("Correo electrónico de la empresa"))
    email_p = models.EmailField(_("Correo personal"))
    tlf_celular=models.TextField(
        _("Teléfono celular"),
        validators=[validators.RegexValidator(
                                    regex=tlf_regex,
                                    message=_('El campo debe ser un número de teléfono'),
                                    code='tlf_celular_invalido'
                                )
                            ])                             
    tlf_local=models.TextField(_("Teléfono local"), validators=[validators.RegexValidator(
                                    regex=tlf_regex,
                                    message=_('El campo debe ser un número de teléfono'),
                                    code='tlf_local_invalido'
                                )
                            ])

    def __str__(self):
        return f"{self.nombre} {self.ci} {self.email_p}"

