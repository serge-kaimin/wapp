# backend_api/views.py
import logging
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from backend_api.serializers import YourModelSerializer  # Use absolute import
from backend_api.api_utils import get_settings_from_api, get_state_instance_from_api, post_message, download_media_by_url, send_file_to_api
from .serializers import RequestSerializer, SendMessageRequestSerializer, SendFileByUrlRequestSerializer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# getSetting
# GET {{apiUrl}}/waInstance{{idInstance}}/getSettings/{{apiTokenInstance}}
# Return settings for the WhatsApp instance
# Required parameters:
#  - idInstance
#  - apiTokenInstance
@csrf_exempt
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
@csrf_exempt
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

    try:
        request_data = json.loads(request.body)
        chat_id = request_data.get('chatId')
        message = request_data.get('message')
        quoted_message_id = request_data.get('quotedMessageId', '')
        link_preview = request_data.get('linkPreview', '')
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON in request body'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # check if chat_id has number@*, if not add @c.us
    if '@' not in chat_id:
        chat_id = f"{chat_id}@c.us"

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

# send_file_by_url
# POST {{mediaUrl}}/waInstance{{idInstance}}/sendFileByUpload/{{apiTokenInstance}}
# Send a file from the WhatsApp instance using a URL
# Required parameters:
#  - idInstance
#  - apiTokenInstance
#  - chatId
#  - url
# Example response:
# {
#    "idMessage": "3EB0C767D097B7C7C030",
#    "urlFile": "https://sw-media-out.storage.yandexcloud.net/1101776123/c1aabd48-c1c2-49b1-8f2d-f575a41777be.jpg"
# }
@csrf_exempt
@require_POST
def send_file_by_url(request):
    id_instance = request.headers.get('idInstance')
    api_token_instance = request.headers.get('apiTokenInstance')

    if not id_instance or not api_token_instance:
        return JsonResponse( 
            {
            'error': 'One ot two mandatory parameters are missing: idInstance and idInstance'
            },
            status=status.HTTP_400_BAD_REQUEST)
    
    try:
        request_data = json.loads(request.body)
        chat_id = request_data.get('chatId').replace('"', '')
        urlFile = request_data.get('urlFile')
        caption = request_data.get('caption', '')
        url_filename = request_data.get('fileName', '')
    except json.JSONDecodeError:
        return JsonResponse(
            {'error': 'Invalid JSON in request body'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # check if chat_id has number@*, if not add @c.us
    if '@' not in chat_id:
        chat_id = f"{chat_id}@c.us"   

    if url_filename == '':
        url_filename = urlFile.split('/')[-1]
        # TODO: detect media format and set the filename accordingly [webp, jpg, png, mp4, etc]
        # for example the media type for the url is webp
        # https://avatars.mds.yandex.net/get-pdb/477388/77f64197-87d2-42cf-9305-14f49c65f1da/s375 
    
    request_data = {
        'chatId': chat_id,
        'urlFile': urlFile,
        'fileName': url_filename,
    }
    if caption != '':
        request_data['caption'] = caption

    logger.info(f"Request to send_file_by_url received: {request_data}")

    serializer = SendFileByUrlRequestSerializer(data=request_data)
    if serializer.is_valid():

        # Download a file from the urlFile
        media_response = download_media_by_url(serializer.validated_data['urlFile'])
        if media_response['status'] != status.HTTP_200_OK:
            return JsonResponse({'error': media_response['error']}, status=media_response['status'])

        MEDIA_FILE_LIMIT=102400 # 100kb
        media_data = media_response.get('media')
        media_size = len(media_data)
        logger.info(f"Meia file downloaded: {url_filename}, [{media_size} bytes] ")
        if media_size == 0:
            return JsonResponse({'error': 'Media file is empty'}, status=status.HTTP_400_BAD_REQUEST)
        if media_size > MEDIA_FILE_LIMIT:
            return JsonResponse({'error': 'Media file is too large limit is {MEDIA_FILE_LIMIT} bytes'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = send_file_to_api(id_instance, api_token_instance, request_data)
        if response['status'] == status.HTTP_200_OK:
            return JsonResponse(response)
        return JsonResponse({'error': response['error']}, status=response['status'])    
    
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
