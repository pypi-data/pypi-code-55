import os
from oauth2client import client, file, tools
from apiclient.discovery import build
import httplib2
from pathlib import Path

# put in path name for secrets et al as running from batch file
########################
pathname = Path(os.path.join(os.path.abspath('')))
########################

# key = 'AIzaSyCl41ZyJ70G9C68DTa8Yo6a-gS1Z9Pxs-g'
CLIENT_ID = os.environ.get('YT_ANALYTICS_CLIENT_ID')
CLIENT_SECRET = os.environ.get('YT_ANALYTICS_CLIENT_SECRET')
ACCESS_TOKEN = os.environ.get('YT_ANALYTICS_ACCESS_TOKEN')
R_TOKEN = os.environ.get('YT_ANALYTICS_REFRESH_TOKEN')


class YoutubeAnalyticsAPI:
    """Create a youtube analytics session using oauth2 flow
    by abstracting this away makes it easier to change the oauth2 flow in the future"""
    def __init__(self, scopes = ['https://www.googleapis.com/auth/yt-analytics.readonly'],
                 secrets_path = pathname / 'youtube_secrets_details.json',
                 analyticsdat = pathname / 'YTanalytics.dat'):
        self.scopes = scopes
        self.secrets_path = secrets_path
        self.initialize_analyticsreporting(analyticsdat)

    def __repr__(self):
        return f'{self.__class__.__name__}(scopes="{self.scopes}"", secrets_path="{self.secrets_path}"'

    def initialize_analyticsreporting(self, analyticsdat):
        credentials = client.OAuth2Credentials(
            ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET, R_TOKEN,
            None, 'https://oauth2.googleapis.com/token', None)
        http = credentials.authorize(httplib2.Http())
        self.analytics = build('youtubeAnalytics', 'v2', http=http)


class YoutubeAPI:
    """Create a youtube analytics session using oauth2 flow
    by abstracting this away makes it easier to change the oauth2 flow in the future"""
    def __init__(self, scopes = ['https://www.googleapis.com/auth/youtube.readonly',
                                 'https://www.googleapis.com/auth/yt-analytics.readonly'],
                 secrets_path = pathname / 'youtube_secrets_details.json',
                 youtubedat = pathname / 'YTanalytics.dat'):
        self.scopes = scopes
        self.secrets_path = secrets_path
        self.initialize_apireporting(youtubedat)

    def __repr__(self):
        return f'{self.__class__.__name__}(scopes="{self.scopes}"", secrets_path="{self.secrets_path}"'

    def initialize_apireporting(self, youtubedat):
        # Parse command-line arguments.
        credentials = client.OAuth2Credentials(
            ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET, R_TOKEN,
            None, 'https://oauth2.googleapis.com/token', None)
        http = credentials.authorize(httplib2.Http())
        self.reports = build('youtube', 'v3', http=http)


