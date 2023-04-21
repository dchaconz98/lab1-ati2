from lab_ati.empresa.views import obtener_informacion_empresa 

class EmpresaGlobalMiddleware:
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        business_id = False
        
        empresa = { "logo" : False }

        print("******************", request.method)
        print(request.GET)
        print(request.POST)
        print("******************", request.path)
        
        idPk =request.path.split('/')
        
        print("====>" , idPk)

        opcion = ['business', 'details', 'edit', 'delete']

        if idPk[1] in 'business':
            
            business_id =idPk[2]
        
            if idPk[2] in opcion:

                business_id = idPk[3] 

        if business_id in 'create' or business_id in opcion:
            
            business_id = False
        

        # Si se proporciona un ID diferente en la consulta GET, utiliza ese ID en su lugar.
        if request.GET.get('empresa'):

            print("entre aqui por lo tanto existe la empresa", request.GET.get('empresa') )

            business_id = request.GET.get('empresa') #request.GET['business_id']
        
        
        if business_id:

            empresa = obtener_informacion_empresa(request,business_id)
            
            request.empresa_global = empresa
        
            response = self.get_response(request)
        
            return response

        request.empresa_global = empresa
        
        response = self.get_response(request)

        return response
    
# class EmpresaGlobalMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
        
#         if hasattr(request, 'empresa_global'):
#             response.context_data['empresa_global'] = request.empresa_global
        
#         return response

# # def empresa_logo(request):
# #     print(request)
# #     business_id = request

# #     """Expose some settings from django-allauth in templates."""
# #     return {
# #         "contextLogo": business_id,
# #     }


""" 
if request.GET.get('business_id'):

            print("entre aqui por lo tanto existe la empresa", request.GET.get('business_id') )

            business_id = request.GET.get('business_id') #request.GET['business_id']

        if request.GET.get('business_id'):

            print("entre aqui por lo tanto existe la empresa", request.GET.get('business_id') )

            business_id = request.GET.get('business_id') #request.GET['business_id']

        if request.POST.get('business_id'):

            print("entre aqui por lo tanto existe la empresa", request.POST.get('business_id') )

            business_id = request.GET.get('business_id') #request.GET['business_id']


 """