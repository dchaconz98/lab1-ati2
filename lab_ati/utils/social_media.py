def add_social_media(model_obj, formset, belongs_to=None):
    """
    Add SocialMedia to Empleado, Empresa, ...
    """

    instances = formset.save(commit=False)
    # Add
    for socialmedia in instances:
        if belongs_to is not None:
            socialmedia.belongs_to = belongs_to
        socialmedia.content_object = model_obj
        socialmedia.save()

    # Delete
    for socialmedia in formset.deleted_objects:
        socialmedia.delete()
