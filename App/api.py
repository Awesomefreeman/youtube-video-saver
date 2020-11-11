import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            pass
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES) 
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


class Request:
    def __init__(self, playlist_id=None, page_token=None):
        # self.part = part
        self.max_result = 50
        self.playlist_id = playlist_id
        self.page_token = page_token
        self.mine = True
        self.snippet = "snippet"
        self.content_details = "contentDetails"
        self.title = []

    def _playlistitems(self):
        request = get_authenticated_service().playlistItems().list(
            part=self.snippet,
            maxResults=self.max_result,
            playlistId=self.playlist_id,
        )
        return request.execute()

    def _next_playlistitems(self, next_page_token):
        request = get_authenticated_service().playlistItems().list(
            part=self.snippet,
            maxResults=self.max_result,
            playlistId=self.playlist_id,
            pageToken=next_page_token
        )
        return request.execute()

    def favorites(self):
        request = get_authenticated_service().channels().list(
            part=self.content_details,
            mine=self.mine
        )
        response = request.execute()
        favorites = response.get("items")[0].get("contentDetails").get("relatedPlaylists").get("favorites")
        return favorites

    def my_playlists(self):
        request = get_authenticated_service().playlists().list(part=self.snippet,
                                                               mine=self.mine,
                                                               maxResults=self.max_result)
        response = request.execute()
        my_playlists = {}
        for r in response['items']:
            my_playlists[r.get("snippet").get("title")] = r.get("id")
            # id_list.append(r.get("id"))
            # title_list.append(r.get("snippet").get("title"))
        return my_playlists

    def my_playlists_title(self):
        request = get_authenticated_service().playlists().list(part=self.snippet,
                                                               mine=self.mine,
                                                               maxResults=self.max_result)
        response = request.execute()
        title = []
        for r in response['items']:
            title.append(r.get("snippet").get("title"))
        return title

    def get_video_id(self):
        response = self._playlistitems()
        next_page_token = response.get("nextPageToken")
        id_list = []
        title = []
        for i in response.get("items"):
            id_list.append(i.get("snippet").get("resourceId").get("videoId"))
            title.append(i.get("snippet").get("title"))
        while next_page_token:
            response = self._next_playlistitems(next_page_token)
            for i in response.get("items"):
                id_list.append(i.get("snippet").get("resourceId").get("videoId"))
                title.append(i.get("snippet").get("title"))
            next_page_token = response.get("nextPageToken")
        return id_list


