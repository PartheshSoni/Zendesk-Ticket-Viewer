"""Main script for running Zendesk Ticket Viewer software."""

import os
import requests
import argparse
import shutil

import display_utils
from exceptions import ZendeskTicketViewerException, ZendeskAPIAccessException

from typing import Union, List, Dict

# Variables to form URLs according to user information
_SINGLE_TICKET_URL = "https://{}.zendesk.com/api/v2/tickets/{}.json"
_ALL_TICKETS_URL = "https://{}.zendesk.com/api/v2/tickets.json"

# Variables to store strings
_TICKET = "ticket"
_TICKETS = "tickets"
_ERROR = "error"

# Size of batch of tickets to display at once.
_DISPLAY_BATCH_SIZE = 25

CLEAR_SCREEN = lambda: os.system("cls") if os.name == "nt" else os.system("clear")


def get_api_error_message(response: requests.Response) -> str:
    """Returns message according to the status code of given 'Response'.

    Args:
        reponse: Instance of requests.Response, returned by GET request.
    Returns:
        String containing the error message.
    """
    error_msg = response.json()[_ERROR]
    if response.status_code == 401:
        return "Looks like your user-ID and/or api-token is wrong.\n{}".format(error_msg)
    elif response.status_code == 403:
        return "Looks like there is no access to the resource that you are trying to request.\n{}".format(error_msg)
    elif response.status_code == 404:
        return "Looks like the resource you are trying to access does not exists.\n{}".format(error_msg)
    else:
        return "Unable to reach Zendesk API, or getting unknown error. Please try after sometime.\n{}".format(error_msg)


def handle_api_failure_reponse(response: requests.Response) -> None:
    """Method to check for problems while accessing the Zendesk API.

    Throws ZendeskAPIAccessException for API access issues.

    Args:
        response: Instance of requests.Response, returned by GET request.
    """
    if response.status_code != 200:
        raise ZendeskAPIAccessException(get_api_error_message(response))


def get_resource_url(sub_domain: str, ticket_id: str = None) -> str:
    """Returns API URL according to given sub-domain and ticket-id.

    If ticket_id is not given, URL to get all tickets is returned.

    Args:
        sub_domain: Sub domain of the account of which tickets are required.
        ticket_id: (Optional) ID of the ticket to be fetched.
    Returns:
        String URL to access the API.
    """ 

    if ticket_id:
        return _SINGLE_TICKET_URL.format(sub_domain, ticket_id)
    else:
        return _ALL_TICKETS_URL.format(sub_domain)


def get_tickets(sub_domain: str, user_id: str, api_token: str, ticket_id: str = None) -> Union[Dict, List[Dict]]:
    """Fetches and returns tickets according to the parameters provided.

    Args:
        sub_domain: Sub domain of the account of which tickets are required.
        user_id: User-ID of the account of which tickets are required.
        api_token: API token of the account of which tickets are required.
    Returns:
        If ticket_id is given, dictionary containing ticket information is returned,
        else list containing dictionary of ticket information is returned.
    """
    url = get_resource_url(sub_domain, ticket_id)
    try:
        response = requests.get(url, auth=("{}/token".format(user_id), api_token))
    except Exception as e:
        raise ZendeskTicketViewerException("An error occurred while accessing the API. "
            "Please check your internet connection or try after sometime.")
    handle_api_failure_reponse(response)
    return response.json()


def run_viewer(sub_domain: str, user_id: str, api_token: str) -> None:
    """Method to accept user commands and execute them in context of Zendesk Ticket Viewer.
    
    Args:
        sub_domain: Sub domain of the account of which tickets are required.
        user_id: User-ID of the account of which tickets are required.
        api_token: API token of the account of which tickets are required.
    """

    print("Type 'menu' to view options or 'quit' to exit")
    while True:
        try:
            command = input("\n\nCommand (type 'menu' for options): ").lower().strip()
            if command == "menu":
                display_utils.display_menu()
            elif command == "1":
                ticket_id = input("Enter a ticket-ID (#): ")
                ticket = get_tickets(sub_domain, user_id, api_token, ticket_id)
                display_utils.display_single_ticket(ticket[_TICKET])
            elif command == "2":
                tickets = get_tickets(sub_domain, user_id, api_token)
                display_utils.display_multiple_tickets(tickets[_TICKETS], _DISPLAY_BATCH_SIZE)
            elif command == "quit":
                return
            else:
                print("You have entered wrong command! Type 'menu' to view valid commands.")
        except ZendeskTicketViewerException as z_tv_e:
            print(z_tv_e)
        except Exception as e:
            print(e)


def get_token(token_file: str) -> str:
    """Reads and returns API token from the token file path given."""
    if not os.path.exists(token_file):
        raise FileNotFoundError("Token file does not exists.")
    with open(token_file, mode="r") as t_file:
        file_lines = []
        for line in t_file:
            file_lines.append(line.strip())
    return file_lines[0]


def main(args: argparse.Namespace) -> None:
    """Main method for Zendesk Ticket Viewer."""
    CLEAR_SCREEN()
    columns = shutil.get_terminal_size().columns
    print("Zendesk Ticket Viewer\n\n".center(columns))
    run_viewer(args.sub_domain, args.user_id, get_token(args.token_file))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments for reading Zendesk tickets")
    parser.add_argument("--sub_domain", type=str, 
                        required=True, help="Sub Domain of the Zendesk account")
    parser.add_argument("--user_id", type=str, required=True, 
                        help="User-ID of the Zendesk account")
    parser.add_argument("--token_file", type=str, required=True, 
                        help="File containing API token of the Zendesk account")
    args = parser.parse_args()

    main(args)    