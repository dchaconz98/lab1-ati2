# Como añadir redes sociales

1) En el contexto de la vista añadir la instancia del formulario


```python
# Importar el formset
from lab_ati.empresa.forms import SocialMediaFormset

# Importar el modelo SocialMedia
from lab_ati.empresa.models import SocialMedia
```

```python
SocialMediaFormset(queryset=SocialMedia.objects.none())
```

Por ejemplo en una vista basada en clases

```python
def get_context_data(self, **kwargs):
  context = super().get_context_data(**kwargs)
  # Queryset vacio porque vamos a crear un empleado nuevo
  context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
  return context
```

2) En el formulario correspondiente de tu vista incluir el template `common/social_media_form.html`

```html
<form method="POST">
  <!--- ... -->
  {% include "common/social_media_form.html" with socialm_formset=socialm_formset%}
  <!--- ... -->
</form>
```

3) En el js del template, instanciar la clase `SocialMediaController;`

```html
{% block inline_javascript %}
<script>
    window.addEventListener('DOMContentLoaded', () => {
        new SocialMediaController();
    });
</script>
{% endblock inline_javascript %}
```

También puede ser un archivo .js

4) En la vista instancia y validar el formulario

```python

# Importar
from lab_ati.utils.social_media import add_social_media
#...

social_media_formset = SocialMediaFormset(data=request.POST)

if social_media_formset.is_valid():
  add_social_media(model_obj, social_media_formset)
```

`model_obj` es la instancia del modelo al que le quieren relacionar las redes sociales, puede ser un Empleado, una Empresa, un Proveedor, ...

## Documentación sobre los formsets

[Using a formset in views and templates](https://docs.djangoproject.com/en/4.0/topics/forms/formsets/#using-a-formset-in-views-and-templates)

[Using the formset in the template | Model Formset](https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/#using-the-formset-in-the-template)
