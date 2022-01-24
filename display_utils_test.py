"""Tests for methods in display_utils.py"""

import unittest
import sys
import display_utils as du

from unittest import mock
from io import StringIO


class TestDisplayUtils(unittest.TestCase):
    def test_display_menu(self):
        expected_calls = [mock.call("\nPlease enter a command from below:"),
        mock.call("-> Enter '1' for fetching a single ticket."),
        mock.call("-> Enter '2' for fetching all tickets."),
        mock.call("-> Enter 'quit' to exit the software.")]
        with mock.patch("builtins.print") as mock_print:        
            du.display_menu()
            mock_print.assert_has_calls(expected_calls)

    def test_display_ticket_for_detailed_view(self):
        mock_ticket = {"id": 1,  "status": "closed", "priority": "high", "assignee_id": 34, "subject": "Test ticket",
         "description": "This is a test description"}

        expected_calls = [mock.call("\nTicket-ID: {}".format(mock_ticket["id"])),
        mock.call("Priority: {}".format(mock_ticket["priority"])),
        mock.call("Status: {}".format(mock_ticket["status"])),
        mock.call("Assignee-ID: {}".format(mock_ticket["assignee_id"])),
        mock.call("Subject: {}".format(mock_ticket["subject"])),
        mock.call("Description: {}".format(mock_ticket["description"]))]

        with mock.patch("builtins.print") as mock_print:        
            du.display_ticket_for_detailed_view(mock_ticket)
            mock_print.assert_has_calls(expected_calls)
        
    def test_display_ticket_for_list_view(self):
        mock_ticket = {"id": 1, "status": "open", "subject": "Test ticket",
         "description": "This is a test description"}
        expected_call = [mock.call("\nTicket-ID: {}, Status: {}, Subject: {}".format(mock_ticket["id"], mock_ticket["status"], mock_ticket["subject"]))]

        with mock.patch("builtins.print") as mock_print:        
            du.display_ticket_for_list_view(mock_ticket)
            mock_print.assert_has_calls(expected_call)

    def test_display_single_ticket(self):
        mock_ticket = mock.Mock()
        with mock.patch.object(du, "display_ticket_for_detailed_view") as display_details:
            du.display_single_ticket(mock_ticket)
            display_details.assert_called_with(mock_ticket)
        

        

if __name__ == '__main__':
    unittest.main()