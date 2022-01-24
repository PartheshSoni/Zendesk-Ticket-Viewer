"""Module containing Exceptions used in Zendesk Ticket Viewer."""

class ZendeskTicketViewerException(Exception):
    """Top level exception for Zendesk Ticket Viewer software."""
    pass

class ZendeskAPIAccessException(ZendeskTicketViewerException):
    """Exception to be thrown when there is some issue while accessing Zendesk API."""
    pass