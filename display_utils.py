"""Utilities for displaying menu and ticket information for Zendesk Ticket Viewer."""

from typing import List, Dict


def display_menu() -> None:
    """Prints Menu option for Zendesk Ticket Viewer."""
    print("\nPlease enter a command from below:")
    print("-> Enter '1' for fetching a single ticket.")
    print("-> Enter '2' for fetching all tickets.")
    print("-> Enter 'quit' to exit the software.")


def display_single_ticket(ticket: Dict) -> None:
    """Calls method to print detailed information of given dictionary."""
    display_ticket_for_detailed_view(ticket)


def display_ticket_for_list_view(ticket: Dict) -> None:
    """Prints information from given ticket dictionary in short."""
    print("\nTicket-ID: {}, Status: {}, Subject: {}".format(
        ticket["id"], ticket["status"], ticket["subject"]))


def display_ticket_for_detailed_view(ticket: Dict) -> None:
    """Prints detailed information of given ticket dictionary"""
    print("\nTicket-ID: {}".format(ticket["id"]))
    print("Priority: {}".format(ticket["priority"]))
    print("Status: {}".format(ticket["status"]))
    print("Assignee-ID: {}".format(ticket["assignee_id"]))
    print("Subject: {}".format(ticket["subject"]))
    print("Description: {}".format(ticket["description"]))


def display_multiple_tickets(tickets: List[Dict], batch_size: int = 25) -> None:
    """Displays multiple ticket on the console.

    Prints tickets in batch of given batch size. Also, option to view a particular ticket
        in detail is present after a batch of tickets is displayed.

    Args:
        tickets: List containing dictionary with ticket information.
        batch_size: Number of tickets to be displayed in a single batch.
    """
    number_of_tickets = len(tickets)
    batch_start = 0
    batch_end = batch_size
    while batch_end <= number_of_tickets:
        for idx in range(batch_start, min(batch_end, number_of_tickets)):
            display_ticket_for_list_view(tickets[idx])
        batch_start = batch_end
        batch_end += batch_size
        quit_to_menu = False
        while True:
            list_command = input("\nEnter 'c' to display more tickets (if any), '<ticket-id>' for detailed view of a ticket, "
                "or 'q' to back to menu commands: ").lower().strip()
            if list_command.isnumeric():
                if int(list_command) <= number_of_tickets:
                    display_ticket_for_detailed_view(tickets[int(list_command) - 1])
                else:
                    print("Ticket with given ticket-id does not exist.")
            elif list_command == "q":
                quit_to_menu = True
                break
            elif list_command == "c":
                break
            else:
                print("Please enter a valid command!")
        if(quit_to_menu):
            break