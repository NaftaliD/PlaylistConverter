from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


def handle_oauth(scope: str) -> InstalledAppFlow.credentials:
    """ Handle OAuth2.0 for the YouTube api.

    Keyword arguments:
    scope: str -- the scope of access for YouTube

    return:
    InstalledAppFlow.credentials -- credantials for opening a connection to the YouTube api
    """

    # token.pickle stores the user's credentials from previously successful logins
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'YouTube_client_secret.json',
                scopes=[
                    scope
                ]
            )

            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                pickle.dump(credentials, f)
    return credentials
