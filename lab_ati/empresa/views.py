from django.http.response import Http404
from django.urls.base import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView, TemplateView
from .forms import CreateBusinessForm, CreateEmployeeForm, SocialMediaFormset
from lab_ati.empresa.models import Empleado, Empresa, SocialMedia
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core import exceptions
from django.shortcuts import render
from lab_ati.utils.social_media import add_social_media
from django.urls import reverse
from django.contrib import messages

# Create your views here.
class BusinessListView(ListView):

    template_name = "pages/business/list.html"
    model = Empresa
    paginate_by = 10


    def get_queryset(self):
        queryset = Empresa.objects.all()
        return queryset

class DeleteBusinessView(DeleteView):
    template_name = "pages/business/delete.html"
    model = Empresa

    def get_success_url(self):
        return reverse('empresa:business-list')

class CreateBusinessView(CreateView):
    template_name = "pages/business/create.html"
    model = Empresa
    form_class = CreateBusinessForm

    def get_success_url(self):
        return reverse(
            "empresa:edit-business",
            kwargs={
                "pk": self.object.pk,
            }
        )

    def post(self, request, *args, **kwargs):
        self.object = None

        self.social_media_formset = SocialMediaFormset(data = self.request.POST)
        
        #Call parent class post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if not self.social_media_formset.is_valid():
            return self.form_invalid(form)
        
        res = super().form_valid(form)
        # Add social media to Empresa
        add_social_media(self.object, self.social_media_formset)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        # Queryset vacio porque vamos a crear una empresa nuevo
        context = super().get_context_data(**kwargs)
        context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
        return context

class EditBusinessView(UpdateView):
    template_name = "pages/business/create.html"
    model = Empresa
    form_class = CreateBusinessForm
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse(
            "empresa:edit-business",
            kwargs={
                "pk": self.object.pk
            }
        )
    
    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.social_media_formset = SocialMediaFormset(
            data=self.request.POST,
            queryset=self.object.redes_sociales.all()
        )
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        if not self.social_media_formset.is_valid():
            return self.media_form_invalid(form)

        # Update and add social media
        add_social_media(self.object, self.social_media_formset)

        res = super().form_valid(form)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def media_form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["socialm_formset"] = SocialMediaFormset(
            queryset=self.object.redes_sociales.all()
        )
        context["editing_social"] = True
        context["business_id"] = self.object.id
        return context

class BusinessDetailsView(DetailView):
    template_name = "pages/business/detail.html"
    model = Empresa

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["business_id"] = self.object.id
        return context


class CreateEmployeeView(CreateView):
    template_name = "pages/employees/create.html"
    model = Empleado
    form_class = CreateEmployeeForm

    def get_success_url(self):
        return reverse(
            "empresa:edit-employee",
            kwargs={
                "business_id": self.empresa.id,
                "pk": self.object.pk,
            },
        )
    def get_empresa(self):

        # Validate that Empresa exists
        try:
            empresa = Empresa.objects.get(id=self.kwargs.get("business_id"))
        except (Empresa.DoesNotExist, exceptions.ValidationError):
            raise Http404(_("La empresa no existe"))

        return empresa

    def post(self, request, *args, **kwargs):
        self.object = None

        # Validate that Empresa exists
        self.empresa = self.get_context_data()["empresa"]

        self.social_media_formset = SocialMediaFormset(data=self.request.POST)

        # Call parent class post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # Override form valid method to add socialmedia
        # functionality

        if not self.social_media_formset.is_valid():
            return self.form_invalid(form)

        res = super().form_valid(form)
        # Add social media to Empleado
        add_social_media(self.object, self.social_media_formset)
        return res

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        context["empresa"] = self.get_empresa()
        context["business_id"] = context["empresa"].id
        # Header
        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["empresa"].id} )
        context["back_link"] = context["list_link"]

        # Queryset vacio porque vamos a crear un empleado nuevo
        context["socialm_formset"] = SocialMediaFormset(queryset=SocialMedia.objects.none())
        return context


class EditEmployeeView(UpdateView):
    template_name = "pages/employees/create.html"
    model = Empleado
    form_class = CreateEmployeeForm
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse(
            "empresa:edit-employee",
            kwargs={
                "business_id": self.empresa.id,
                "pk": self.object.pk,
            },
        )

    def get_empresa(self):

        # Validate that Empresa exists
        try:
            empresa = Empresa.objects.get(id=self.kwargs.get("business_id"))
        except (Empresa.DoesNotExist, exceptions.ValidationError):
            raise Http404(_("La empresa no existe"))

        return empresa

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.empresa = self.get_empresa()
        self.social_media_formset = SocialMediaFormset(
            data=self.request.POST,
            queryset=self.object.redes_sociales.all()
        )
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):

        if not self.social_media_formset.is_valid():
            return self.media_form_invalid(form)

        # Update and add social media
        add_social_media(self.object, self.social_media_formset)

        res = super().form_valid(form)
        return res

    def media_form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                socialm_formset=self.social_media_formset
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        context["empresa"] = self.get_empresa()
        context["socialm_formset"] = SocialMediaFormset(
            queryset=self.object.redes_sociales.all()
        )
        context["editing_social"] = True

        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["empresa"].id} )
        context["back_link"] = context["list_link"]

        return context


class ListEmployeeView(ListView):
    template_name = "pages/employees/list.html"
    model = Empleado
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        return context

    def get_queryset(self):
        queryset = Empleado.objects.filter(empresa = self.kwargs['business_id'])
        return queryset


class DeleteEmployeeView(DeleteView):
    template_name = "pages/employees/delete.html"
    model = Empleado

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']
        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["business_id"]} )
        context["back_link"] = context["list_link"]
        return context

    def get_success_url(self):
        return reverse('empresa:list-employee', kwargs={ 'business_id': self.kwargs['business_id']})

class DetailEmployeeView(DetailView):
    template_name = "pages/employees/detail.html"
    model = Empleado
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['business_id'] = self.kwargs['business_id']

        context["list_link"] = reverse("empresa:list-employee", kwargs={"business_id": context["business_id"]} )
        context["back_link"] = context["list_link"]
        return context


def actualizar_logo_empresa(request, business_id):

    print("actualizar_logo_empresa")
    empresa =Empresa.objects.get(pk=business_id) # get_object_or_404(Empresa, id=business_id)

    if request.method == 'POST' and empresa:

        imagen = request.FILES['logo_business_pk']
        
        if imagen:
            empresa.logo = imagen

            empresa.save(update_fields=['logo'])
            
            request.empresa_global = empresa

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def obtener_informacion_empresa(request, business_id):

    if business_id: 
        
        empresa = Empresa.objects.get(id=business_id)
    
    return empresa 

