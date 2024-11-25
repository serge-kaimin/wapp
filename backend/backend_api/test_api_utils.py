# test_api_utils.py
import unittest
from unittest.mock import patch
from backend_api.api_utils import get_settings_from_api

class TestGetSettingsFromAPI(unittest.TestCase):
    @patch('backend_api.api_utils.requests.get')
    def test_get_settings_from_api_success(self, mock_get):
        # Mock response data
        mock_response_data = {
            "wid": "11001234567@c.us",
            "countryInstance": "",
            "typeAccount": "",
            "webhookUrl": "https://mysite.com/webhook/green-api/",
            "webhookUrlToken": "",
            "delaySendMessagesMilliseconds": 5000,
            "markIncomingMessagesReaded": "no",
            "markIncomingMessagesReadedOnReply": "no",
            "sharedSession": "no",
            "outgoingWebhook": "yes",
            "outgoingMessageWebhook": "yes",
            "outgoingAPIMessageWebhook": "yes",
            "incomingWebhook": "yes",
            "deviceWebhook": "no",
            "statusInstanceWebhook": "no",
            "stateWebhook": "no",
            "enableMessagesHistory": "no",
            "keepOnlineStatus": "no",
            "pollMessageWebhook": "no",
            "incomingBlockWebhook": "yes",
            "incomingCallWebhook": "yes"
        }

        # Configure the mock to return a response with the mock data
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        # Call the function
        id_instance = '12345'
        api_token_instance = 'your_api_token'
        response = get_settings_from_api(id_instance, api_token_instance)

        # Assert the response
        self.assertEqual(response['status'], 200)
        self.assertEqual(response['data'], mock_response_data)

    @patch('backend_api.api_utils.requests.get')
    def test_get_settings_from_api_failure(self, mock_get):
        # Configure the mock to return a response with a 404 status code
        mock_get.return_value.status_code = 404

        # Call the function
        id_instance = '12345'
        api_token_instance = 'your_api_token'
        response = get_settings_from_api(id_instance, api_token_instance)

        # Assert the response
        self.assertEqual(response['status'], 404)
        self.assertEqual(response['error'], 'An error occurred')

if __name__ == '__main__':
    unittest.main()