"""Tests for methods in zendesk_ticket_viewer.py"""

import unittest
import requests
import tempfile
import zendesk_ticket_viewer as ztv
from unittest import mock
from exceptions import ZendeskAPIAccessException

class TestZendeskTicketViewer(unittest.TestCase):
    @mock.patch("requests.Response")
    def test_get_api_error_message_401(self, mock_response):
        mock_response.json.return_value = {"error": "Unknown Error"}
        mock_response.status_code = 401
        expected_output = "Looks like your user-ID and/or api-token is wrong.\nUnknown Error"
        self.assertEqual(ztv.get_api_error_message(mock_response), expected_output)
    
    @mock.patch("requests.Response")
    def test_get_api_error_message_403(self, mock_response):
        mock_response.json.return_value = {"error": "Unknown Error"}
        mock_response.status_code = 403
        expected_output = "Looks like there is no access to the resource that you are trying to request.\nUnknown Error"
        self.assertEqual(ztv.get_api_error_message(mock_response), expected_output)

    @mock.patch("requests.Response")
    def test_get_api_error_message_unknown(self, mock_response):
        mock_response.json.return_value = {"error": "Unknown Error"}
        mock_response.status_code = 406
        expected_output = "Unable to reach Zendesk API, or getting unknown error. Please try after sometime.\nUnknown Error"
        self.assertEqual(ztv.get_api_error_message(mock_response), expected_output)

    @mock.patch("requests.Response")
    def test_get_api_error_message_404(self, mock_response):
        mock_response.json.return_value = {"error": "Unknown Error"}
        mock_response.status_code = 404
        expected_output = "Looks like the resource you are trying to access does not exists.\nUnknown Error"
        self.assertEqual(ztv.get_api_error_message(mock_response), expected_output)

    @mock.patch.object(ztv, "get_api_error_message")
    @mock.patch("requests.Response")
    def test_handle_api_failure_reponse_other_errors(self, mock_response, mock_get_api_error_message):
        mock_response.return_value = 500
        mock_get_api_error_message.return_value = "Internal Server Error!"
        with self.assertRaises(ZendeskAPIAccessException, msg="Internal Server Error!"):
            ztv.handle_api_failure_reponse(mock_response)

    def test_get_resource_url_single_ticket(self):
        expected_output = "https://test_domain.zendesk.com/api/v2/tickets/12.json"
        self.assertEqual(ztv.get_resource_url(sub_domain="test_domain", ticket_id=12), expected_output)

    def test_get_resource_url_all_ticket(self):
        expected_output = "https://test_domain.zendesk.com/api/v2/tickets.json"
        self.assertEqual(ztv.get_resource_url(sub_domain="test_domain"), expected_output)

    @mock.patch.object(ztv, "get_resource_url")
    @mock.patch.object(requests, "get")
    @mock.patch.object(ztv, "handle_api_failure_reponse")
    @mock.patch("requests.Response")
    def test_get_tickets(self, mock_response, mock_api_prob, mock_req_get, mock_res_url):
        test_subdomain = "test_domain"
        test_user = "test_user"
        test_token = "test_token"
        test_ticket_num = 2
        mock_response.json.return_value = "test_json"
        mock_res_url.return_value = "test_url"
        mock_req_get.return_value = mock_response

        self.assertEqual(ztv.get_tickets(test_subdomain, test_user, test_token, test_ticket_num), "test_json")
        mock_res_url.assert_called_with(test_subdomain, test_ticket_num)
        mock_req_get.assert_called_with("test_url", auth=("test_user/token", test_token))
        mock_api_prob.assert_called_with(mock_response)

    def test_get_token(self):
        test_token_file = tempfile.NamedTemporaryFile()
        with open(test_token_file.name, "w") as tf:
            tf.write("Test token")
        self.assertEqual(ztv.get_token(test_token_file.name), "Test token")
        

if __name__ == '__main__':
    unittest.main()
