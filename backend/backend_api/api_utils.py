# backend_api/api_utils.py
import requests
import time
import logging

from django.http import JsonResponse
from rest_framework import status
from .serializers import SettingsResponseSerializer, StateInstanceResponseSerializer, SendMessageResponseSerializer, SendFileByUrlRequestSerializer
from .errors import process_error
# from rest_framework.response import Response  # Import Response

API_URL = 'https://7103.api.greenapi.com'
MEDIA_URL = 'https://7103.media.greenapi.com'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#  getSettings
#  GET {{apiUrl}}/waInstance{{idInstance}}/getSettings/{{apiTokenInstance}}
#  Required parameters:
#  - idInstance
#  - apiTokenInstance
#  Response: JSON
#  Serializer: SettingsResponseSerializer
#  reference: https://green-api.com/docs/api/account/GetSettings/
def get_settings_from_api(id_instance, api_token_instance):
    api_url = f"{API_URL}/waInstance{id_instance}/getSettings/{api_token_instance}"

    payload = {}
    headers= {}

    # Measure the start time
    start_time = time.time()

    response_data = requests.request("GET", api_url, headers=headers, data = payload)

     # Measure the end time
    end_time = time.time()
    request_time = end_time - start_time

    # Log the request time
    logger.info(f"Request getSettings to {API_URL} took {request_time:.2f} seconds")
    
    if response_data.status_code == 200:
        try:
            response_json = response_data.json()
            serializer = SettingsResponseSerializer(data=response_json)
            if serializer.is_valid():
                return {
                    'message': 'Success',
                    'data': serializer.validated_data,
                    'status': 200
                }
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return {
                    'error': 'Invalid response data',
                    'details': serializer.errors,
                    'status': 500
                }
        except requests.exceptions.JSONDecodeError:
            return {
                'error': 'Invalid JSON response',
                'status': 500
            }
    else:
        try:
            error_message = response_data.json().get('error', None)
        except requests.exceptions.JSONDecodeError:
            error_message = None
        return {
            'error': process_error(response_data.status_code, error_message),
            'status': response_data.status_code
        }


# getStateInstance
# GET {{apiUrl}}/waInstance{{idInstance}}/getStateInstance/{{apiTokenInstance}}
#  Required parameters:
#  - idInstance
#  - apiTokenInstance
#  Response: JSON
#  Serializer: SettingsResponseSerializer
#  reference: https://green-api.com/docs/api/account/GetStateInstance/
def get_state_instance_from_api(id_instance, api_token_instance):
    api_url = f"{API_URL}/waInstance{id_instance}/getStateInstance/{api_token_instance}"

    payload = {}
    headers= {}

    # Measure the start time
    start_time = time.time()

    response_data = requests.request("GET", api_url, headers=headers, data = payload)

    # Measure the end time
    end_time = time.time()
    request_time = end_time - start_time

    # Log the request time
    logger.info(f"Request getStateInstance to {API_URL} took {request_time:.2f} seconds")

    if response_data.status_code == status.HTTP_200_OK:
        try:
            response_json = response_data.json()
            serializer = StateInstanceResponseSerializer(data=response_json)
            if serializer.is_valid():
                return {
                    'message': 'Success',
                    'data': serializer.validated_data,
                    'status': status.HTTP_200_OK
                }
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return {
                    'error': 'Invalid response data',
                    'details': serializer.errors,
                    'status': status.HTTP_400_BAD_REQUEST
                }
        except requests.exceptions.JSONDecodeError:
            return {
                'error': 'Invalid JSON response',
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
    else:
        try:
            error_message = response_data.json().get('error', None)
        except requests.exceptions.JSONDecodeError:
            error_message = None
        return {
            'error': process_error(response_data.status_code, error_message),
            'status': response_data.status_code
        }
# post_message
# POST {{apiUrl}}/waInstance{{idInstance}}/sendMessage/{{apiTokenInstance}}
# Required parameters:
# - idInstance
# - apiTokenInstance
# - chatId
# - message
# Response: JSON
# Serializer: SendMessageRequestSerializer
# reference: https://green-api.com/docs/api/message/SendMessage/
def post_message(id_instance, api_token_instance, request_data):
    api_url = f"{API_URL}/waInstance{id_instance}/sendMessage/{api_token_instance}"

    payload = request_data
    headers = {
        'Content-Type': 'application/json'
    }

    # Measure the start time
    start_time = time.time()
    logger.info(f"payload: {payload}")

    response_data = requests.post(api_url, json=payload, headers=headers)

    logger.info(f"Response received: {response_data}")

    # Measure the end time
    end_time = time.time()
    request_time = end_time - start_time

    # Log the request time
    logger.info(f"Request to {API_URL} took {request_time:.2f} seconds")

    if response_data.status_code == 200:
        try:
            response_json = response_data.json()
            serializer = SendMessageResponseSerializer(data=response_json)
            if serializer.is_valid():
                return {
                    'message': 'Success',
                    'data': serializer.validated_data,
                    'status': 200
                }
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return {
                    'error': 'Invalid response data',
                    'details': serializer.errors,
                    'status': 500
                }
        except requests.exceptions.JSONDecodeError:
            return {
                'error': 'Invalid JSON response',
                'status': 500
            }
    else:
        try:
            error_message = response_data.json().get('error', None)
        except requests.exceptions.JSONDecodeError:
            error_message = None
        return {
            'error': process_error(response_data.status_code, error_message),
            'status': response_data.status_code
        }

# download_media_by_url
# Download a file from the URL
def download_media_by_url(url):
    try :
        response = requests.get(url)
        status_code = response.status_code

        # Define a dictionary to map status codes to their corresponding actions
        status_actions = {
            status.HTTP_200_OK: {
                'status': status.HTTP_200_OK,
                'media': response.content  # Return the raw content of the media
            },
            status.HTTP_404_NOT_FOUND: {
                'status': status.HTTP_404_NOT_FOUND,
                'error': 'Media not found'
            },
            status.HTTP_403_FORBIDDEN: {
                'status': status.HTTP_403_FORBIDDEN,
                'error': 'Access to media is forbidden'
            },
        }

        # Return the corresponding action for the status code, or a default error
        return status_actions.get(status_code, {
            'status': status_code,
            'error': response.text
        })
    except requests.exceptions.RequestException as e:
        return {
            'error': 'Error downloading media',
            'details': str(e),
            'status': 500
        }

# SendFileByUrl
# POST {{apiUrl}}/waInstance{{idInstance}}/sendFileByUrl/{{apiTokenInstance}}
# Required parameters:
# - idInstance
# - apiTokenInstance
# - chatId
# - urlFile
# - fileName
# - caption (optional)
# - quotedMessageId (optional)
# RESPONSE: JSON
# Serializer: SendFileByUrlRequestSerializer
# Example response:
# {
#    "idMessage": "3EB0C767D097B7C7C030"
# }
def send_file_to_api(id_instance, api_token_instance, request_data):
    api_url = f"{API_URL}/waInstance{id_instance}/sendFileByUrl/{api_token_instance}"

    payload = request_data
    headers = {
        'Content-Type': 'application/json'
    }

    # Measure the start time
    start_time = time.time()
    logger.info(f"payload: {payload}")

    response_data = requests.post(api_url, json=payload, headers=headers)

    logger.info(f"Response received: {response_data}")

    # Measure the end time
    end_time = time.time()
    request_time = end_time - start_time

    # Log the request time
    logger.info(f"Request send_file_by_url to {API_URL} took {request_time:.2f} seconds")

    if response_data.status_code == 200:
        try:
            response_json = response_data.json()
            serializer = SendMessageResponseSerializer(data=response_json)
            if serializer.is_valid():
                return {
                    'message': 'Success',
                    'data': serializer.validated_data,
                    'status': 200
                }
            else:
                logger.error(f"Validation errors: {serializer.errors}")
                return {
                    'error': 'Invalid response data',
                    'details': serializer.errors,
                    'status': 500
                }
        except requests.exceptions.JSONDecodeError:
            return {
                'error': 'Invalid JSON response',
                'status': 500
            }
    else:
        try:
            error_message = response_data.json().get('error', None)
        except requests.exceptions.JSONDecodeError:
            error_message = None
        return {
            'error': process_error(response_data.status_code, error_message),
            'status': response_data.status_code
        }

