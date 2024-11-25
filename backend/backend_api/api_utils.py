# backend_api/api_utils.py
import requests
import time
import logging

from django.http import JsonResponse
from rest_framework import status
from .serializers import SettingsResponseSerializer
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
    logger.info(f"Request to {API_URL} took {request_time:.2f} seconds")
    
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

        