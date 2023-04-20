



def empresa_logo(request):
    print(request)
    business_id = request

    """Expose some settings from django-allauth in templates."""
    return {
        "contextLogo": business_id,
    }