from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from gmusicapi import Mobileclient


class GspotyException(Exception):
    pass


class Gspoty(object):
    def __init__(self, spotify_client_id, spotify_secret, google_music_device_id):
        self.spotify_client_id = spotify_client_id
        self.spotify_secret = spotify_secret
        self.google_music_device_id = google_music_device_id

    def connect_services(self):
        if not self.google_music_device_id or not self.spotify_client_id or not self.spotify_secret:
            raise GspotyException(
                "Can't authenticate! please provide valid secrets and ids")
        self.sp = Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=self.spotify_client_id, client_secret=self.spotify_secret))
        self.gmapi = Mobileclient(debug_logging=False)
        self.gmapi.oauth_login(self.google_music_device_id)
        # TODO: Verify connection

    def get_spotify_playlist_id(self, spotify_playlist_uri):
        return spotify_playlist_uri.split('/')[-1]

    def get_spotify_search_keys(self, spotify_playlist_id):
        search_keys = []
        try:
            res = self.sp.playlist(playlist_id=spotify_playlist_id,
                                   fields='tracks.items.track(album(id,name),artists(id,name),name,track_number,id)')
            for t in res['tracks']['items']:
                track = t['track']
                album = track['album']
                artists = track['artists']
                track_name = track['name']
                track_number = track['track_number']
                track_id = track['id']
                print("%d - %s / %s (%s)" %
                      (track_number, track_name, artists[0]['name'], track_id))
                search_key = "%s %s %s" % (
                    track_name, album['name'], artists[0]['name'])
                search_keys.append(search_key)
        except SpotifyException as arg:
            print("Error trying to the list %s details: %s" %
                  (spotify_playlist_id, str(arg)))
            raise GspotyException(
                "There was an error with Spotify communication", arg)
        return search_keys

    def get_if_exists(self, spotify_playlist_id):
        playlists = self.gmapi.get_all_playlists()
        playlist_in_gmusic = None

        for p in playlists:
            if p['name'] == spotify_playlist_id:
                playlist_in_gmusic = p

        return playlist_in_gmusic

    def build_gmusic_playlist(self, search_keys, spotify_playlist_id):
        existent_playlist = self.get_if_exists(spotify_playlist_id)
        if existent_playlist:
            print("The playlist already exists" +
                  str(self.get_shareable_link(existent_playlist)))
            return existent_playlist

        g_music_playlist_id = self.gmapi.create_playlist(
            spotify_playlist_id, description="Imported from spotify", public=False)

        for search_key in search_keys:
            r = self.gmapi.search(search_key, max_results=1)
            try:
                if r['song_hits']:
                    found_track = r['song_hits'][0]['track']
                    f_title = found_track['title']
                    f_album = found_track['album']
                    f_artist = found_track['artist']
                    f_store_id = found_track['storeId']
                    print("For Spotify([%s]) in Google Music there is %s %s %s (%s)" %
                          (search_key, f_title, f_album, f_artist, f_store_id))
                    self.gmapi.add_songs_to_playlist(
                        g_music_playlist_id, f_store_id)
                else:
                    print("Did NOT found a song for %s in Google Music" % (search_key))
            except Exception as e:
                print("Something goes wrong with " + search_key)
                print("Details " + str(e))

        existent_playlist = self.get_if_exists(spotify_playlist_id)
        if existent_playlist:
            return existent_playlist
        else:
            raise GspotyException(
                "Endpoint called but no playlist was created")

    def get_shareable_link(self, gmusic_playlist):
        share_token = gmusic_playlist["shareToken"]
        return "https://play.google.com/music/playlist/{}".format(share_token)
