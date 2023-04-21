from django import forms
from lab_ati.cliente.models import Cliente

class ClienteForm(forms.ModelForm):

    # Validación de teléfonos
    def clean(self):
        cleaned_data = super().clean()
        tlf_celular = cleaned_data.get('tlf_celular')
        whatsapp = cleaned_data.get('whatsapp')
        
        # Verificar que al menos un campo no está vacío
        if not tlf_celular and not whatsapp:
           msg = ('Debe ingresar al menos un número de teléfono')
           self.add_error('tlf_celular', msg)
           self.add_error('whatsapp', msg)
        
        return cleaned_data

    class Meta:
        model = Cliente
        fields = '__all__'