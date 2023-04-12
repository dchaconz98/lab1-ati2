from django.shortcuts import render, redirect
from django.http import HttpResponse
from lab_ati.cliente.models import Cliente
from lab_ati.cliente.forms import ClienteForm
from lab_ati.empresa.forms import SocialMediaFormset
from lab_ati.empresa.models import SocialMedia
from lab_ati.utils.social_media import add_social_media
from django.urls import reverse

def clientes(request, business_id):
    context = {}
    context['business_id'] = business_id
    clientes = Cliente.objects.filter(empresa__id__contains = business_id)
    context['clientes'] = clientes
    return render(request, 'pages/clientes/index.html', context)

def ver_cliente(request, id, business_id):
    context = {}
    context['business_id'] = business_id
    cliente = Cliente.objects.get(id = id)
    context['form'] = ClienteForm(request.POST or None, instance=cliente)
    context['social_medias'] = cliente.redes_sociales.all()
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    return render(request, 'pages/clientes/verCliente.html', context)

def crear_cliente(request, business_id):
    context = {}
    context['business_id'] = business_id
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        savedForm = form.save()
        social_media_formset = SocialMediaFormset(data=request.POST)
        if social_media_formset.is_valid():
            add_social_media(savedForm, social_media_formset)
        return redirect('clients', business_id = business_id)
    context['form'] = form
    context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context['business_id'] = business_id
    return render(request, 'pages/clientes/crear.html', context)


def eliminar_cliente(request, id, business_id):
    cliente = Cliente.objects.get(id = id)
    cliente.delete()
    context = {}
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context['business_id'] = business_id
    return redirect('clients', business_id = business_id)

def editar_cliente(request, id, business_id):
    context = {}
    context['business_id'] = business_id
    cliente = Cliente.objects.get(id = id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid() and request.POST:
        savedForm = form.save()
        social_media_formset = SocialMediaFormset(data=request.POST, queryset=savedForm.redes_sociales.all())
        if social_media_formset.is_valid():
            add_social_media(savedForm, social_media_formset)

        return redirect('clients', business_id = business_id)
    context['form'] = form
    context["socialm_formset"] = SocialMediaFormset(queryset=cliente.redes_sociales.all())
    context["list_link"] = reverse("clients", kwargs={"business_id": business_id} )
    context["editing_social"] = True

    return render(request, 'pages/clientes/editar.html', context)
