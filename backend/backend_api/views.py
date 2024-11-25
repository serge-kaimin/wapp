# backend_api/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response  # Import Response
from backend_api.models import YourModel  # Use absolute import
from backend_api.serializers import YourModelSerializer  # Use absolute import
from backend_api.api_utils import get_settings_from_api, get_state_instance_from_api
from .serializers import RequestSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer


# Required parameters:
#  - idInstance
#  - apiTokenInstance
@require_GET
def get_setting(request):

    id_instance = request.headers.get('idInstance')
    api_token_instance = request.headers.get('apiTokenInstance')

    if not id_instance or not api_token_instance:
        return JsonResponse( 
            {
            'error': 'One ot two mandatory parameters are missing: idInstance and idInstance'
            },
            status=status.HTTP_400_BAD_REQUEST)

    data = {
        'id_instance': id_instance,
        'api_token_instance': api_token_instance
    }
    
    serializer = RequestSerializer(data=data)
    if serializer.is_valid():
        id_instance = serializer.validated_data['id_instance']
        api_token_instance = serializer.validated_data['api_token_instance']

        response = get_settings_from_api(id_instance, api_token_instance)
        # need to check response status
        if response['status'] == status.HTTP_200_OK:
            #return JsonResponse({'message': 'Success', 'data': response}, status=status.HTTP_200_OK)
            return JsonResponse(response)
        
        return JsonResponse({'error': response['error']}, status=response['status'])
    
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@require_GET
def get_state_instance(request):

    id_instance = request.headers.get('idInstance')
    api_token_instance = request.headers.get('apiTokenInstance')

    if not id_instance or not api_token_instance:
        return JsonResponse( 
            {
            'error': 'One ot two mandatory parameters are missing: idInstance and idInstance'
            },
            status=status.HTTP_400_BAD_REQUEST)

    data = {
        'id_instance': id_instance,
        'api_token_instance': api_token_instance
    }

    serializer = RequestSerializer(data=data)
    if serializer.is_valid():
        id_instance = serializer.validated_data['id_instance']
        api_token_instance = serializer.validated_data['api_token_instance']

        response = get_state_instance_from_api(id_instance, api_token_instance)
        # need to check response status
        if response['status'] == status.HTTP_200_OK:
            #return JsonResponse({'message': 'Success', 'data': response}, status=status.HTTP_200_OK)
            return JsonResponse(response)
        
        return JsonResponse({'error': response['error']}, status=response['status'])
    
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
