__author__ = 'anish'

"""
The point of this file is to abstract youtube login and interaction
"""

import sys
import httplib2

# Google imports
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = "Missing client secrets"


def get_credentials(args):

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SCOPE)
    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return credentials


def get_youtube_session():

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=get_credentials("").authorize(httplib2.Http()))


def videos(youtube, uid):

    initial = youtube.playlistItems().list(part="snippet", maxResults=50,
                                           playlistId=uid).execute()
    yield initial
    while "nextPageToken" in initial:
        initial = youtube.playlistItems().list(part="snippet", maxResults=50,
                                           playlistId=uid,
                                           pageToken=initial["nextPageToken"]).execute()
        yield initial