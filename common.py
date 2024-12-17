import os
import pickle

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API utils
from googleapiclient.discovery import build

load_dotenv()

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ["https://mail.google.com/"]

DATA_DIR = os.environ["DATA_DIR"]
TOKEN_PICKLE_PATH = os.path.join(DATA_DIR, "token.pickle")
CREDENTIALS_JSON_PATH = os.path.join(DATA_DIR, "credentials.json")


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(TOKEN_PICKLE_PATH):
        with open(TOKEN_PICKLE_PATH, "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_JSON_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(TOKEN_PICKLE_PATH, "wb") as token:
            pickle.dump(creds, token)
    return build("gmail", "v1", credentials=creds)


def search_messages(service, query):
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = []
    if "messages" in result:
        messages.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=page_token)
            .execute()
        )
        if "messages" in result:
            messages.extend(result["messages"])
    return messages
