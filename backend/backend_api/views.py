# backend_api/views.py
import logging
import html
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response  # Import Response
from backend_api.models import YourModel  # Use absolute import
from backend_api.serializers import YourModelSerializer  # Use absolute import
from backend_api.api_utils import get_settings_from_api, get_state_instance_from_api, post_message
from .serializers import RequestSerializer, SendMessageRequestSerializer

class YourModelViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = YourModelSerializer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# getSetting
# GET {{apiUrl}}/waInstance{{idInstance}}/getSettings/{{apiTokenInstance}}
# Return settings for the WhatsApp instance
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

# getStateInstance
# GET {{apiUrl}}/waInstance{{idInstance}}/getStateInstance/{{apiTokenInstance}}
# Return the state of the WhatsApp instance
# Required parameters:
#  - idInstance
#  - apiTokenInstance
# Example response:
# { "stateInstance": "authorized" }
# Reference: https://green-api.com/docs/api/account/GetStateInstance/
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

    request_data = {
        'id_instance': id_instance,
        'api_token_instance': api_token_instance
    }

    serializer = RequestSerializer(data=request_data)
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

# send_message
# POST {{apiUrl}}/waInstance{{idInstance}}/sendMessage/{{apiTokenInstance}}
# Send a message from the WhatsApp instance
# Required parameters:
#  - idInstance
#  - apiTokenInstance
# Example response:
# {
#    "idMessage": "3EB0C767D097B7C7C030"
# }
@csrf_exempt
@require_POST
def send_message(request):

    id_instance = request.headers.get('idInstance')
    api_token_instance = request.headers.get('apiTokenInstance')

    if not id_instance or not api_token_instance:
        return JsonResponse( 
            {
            'error': 'One ot two mandatory parameters are missing: idInstance and idInstance'
            },
            status=status.HTTP_400_BAD_REQUEST)

    #chat_id = request.POST.get('chatId')
    chat_id = request.POST.get('chatId', '').replace('"', '')
    message = request.POST.get('message')
    quoted_message_id = request.POST.get('quotedMessageId', '')
    link_preview = request.POST.get('linkPreview', '')

    request_data = {
        'chatId': chat_id,
        'message': message,
    }

    # Add request data if the optional parameters are not empty
    if quoted_message_id != '':
        request_data['quotedMessageId'] = quoted_message_id
    if link_preview != '':
        request_data['linkPreview'] = link_preview

    logger.info(f"Request received: {request_data}")

    serializer = SendMessageRequestSerializer(data=request_data)
    if serializer.is_valid():

        response = post_message(id_instance, api_token_instance, request_data )
        if response['status'] == status.HTTP_200_OK:
            return JsonResponse(response)        
        return JsonResponse({'error': response['error']}, status=response['status'])
    
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
