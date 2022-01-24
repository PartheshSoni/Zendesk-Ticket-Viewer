## Zendesk Ticket Viewer

Zendesk Ticket Viewer is a lightweight commandline client for fetching and displaying tickets from a Zendesk account provided by the user. It can fetch and print detailed information of a ticket based on the given Ticket-ID, or it can fetch and display all the tickets from an account (in batches of 25) in a list view. User can select and view a ticket in detail view from the list.

The software is created using modular and testable code, and unit tests covering the codebase are included in the repo.

### Requirements
- Python 3 or above.
- Requests module: `pip install requests`


### Before running the software
- Download and unzip the code repo.
- Create an account on Zendesk and (create and) load the tickets.
- Get API token for the account. Make sure tokens are created and enabled (from Admin Center -> Apps and Integration -> Zendesk API). Currently, the software only supports API tokens to authenticate users.
- Copy and save the API token to a file.

### Running Zendesk Ticket Viewer
`python3 zendesk_ticket_viewer.py --sub_domain <zendesk_sub_domain> --user_id <zendesk_user_id> --token_file <path_to_token_file>`

### Running the tests
`python3 zendesk_ticket_viewer_test.py`
`python3 display_utils_test.py`



