from lab_ati.empresa.views import obtener_informacion_empresa 


class EmpresaGlobalMiddleware:
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
    
        business_id = 'create'
        
        empresa = { "id" : False }

        #print("******************", request.method)
        #print(request.GET)
        #print(request.POST)
        #print("******************", request.path)
        
        if request.path == '/':
            
            request.empresa_global = empresa

            response = self.get_response(request)

            return response

        idPk =request.path.split('/')

        opcion = ['business', 'details', 'edit', 'delete', 'guardar-logo']

        if idPk[1] in 'business':
            
            business_id =idPk[2]
        
            if idPk[2] in opcion:

                business_id = idPk[3] 

        if business_id in 'create' or business_id in opcion:
            #print("====> false" , business_id)
            business_id = False
        

        # Si se proporciona un ID diferente en la consulta GET, utiliza ese ID en su lugar.
        if request.GET.get('empresa'):

            #print("entre aqui por lo tanto existe la empresa", request.GET.get('empresa') )

            business_id = request.GET.get('empresa') #request.GET['business_id']
        
        
        if business_id:

            empresa = obtener_informacion_empresa(request,business_id)
            
            request.empresa_global = empresa
        
            response = self.get_response(request)

            return response


        request.empresa_global = empresa

        response = self.get_response(request)
                
        return response
    