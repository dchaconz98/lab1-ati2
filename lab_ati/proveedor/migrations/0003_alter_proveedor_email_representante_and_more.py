# Generated by Django 4.0.5 on 2023-04-22 08:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proveedor', '0002_alter_proveedor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='email_representante',
            field=models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator(code='correo_invalido', message='El campo debe ser un correo valido', regex="^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")], verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='tlf',
            field=models.TextField(validators=[django.core.validators.RegexValidator(code='tlf_invalido', message='El campo debe ser un número de teléfono', regex='^\\+?([0-9]{1,3}|[1]\\-?[0-9]{3})?\\-?([0-9]{1,4})\\-?([0-9]{3}\\-?[0-9]{2}\\-?[0-9]{2})$')], verbose_name='Teléfono del proveedor'),
        ),
    ]