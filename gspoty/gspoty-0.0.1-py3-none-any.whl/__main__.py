#!/usr/bin/env python
if __name__ == "__main__":
    import os
    import sys
    import json
    from . import Gspoty, GspotyException
    SPOTIPY_CLIENT_ID = 'SPOTIPY_CLIENT_ID'
    SPOTIPY_CLIENT_SECRET = 'SPOTIPY_CLIENT_SECRET'
    GOOGLE_MUSIC_DEVICE_ID = 'GOOGLE_MUSIC_DEVICE_ID'

    
    if len(sys.argv) < 2:
        print("""usage: python gspoty playlist_uri [keys_file]
        playlist_uri:\tA valid spotify playlist
        keys_file:\tA valid json file with the keys (default: keys.json)""")
        exit(1)
    playlist_uri = sys.argv[1]

    keys_file = 'keys.json'
    if len(sys.argv) > 2:
        keys_file = sys.argv[2]

    if not os.path.isfile(keys_file) or not os.access(keys_file, os.R_OK):
        print("There is no `{}` to read client keys from".format(keys_file))
        exit(2)

    client_secret_id = {}
    with open(keys_file, 'r', encoding="UTF-8") as k:
        keys = json.load(k)

        for i in [SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, GOOGLE_MUSIC_DEVICE_ID]:
            if keys[i] is None:
                print("The attribute {} is not present".format(i))
                exit(3)
            client_secret_id[i] = keys[i]

    try:
        gspoty = Gspoty(client_secret_id[SPOTIPY_CLIENT_ID],
                        client_secret_id[SPOTIPY_CLIENT_SECRET], client_secret_id[GOOGLE_MUSIC_DEVICE_ID])
        gspoty.connect_services()
        print("Connected to Spotify and Google Music")
        playlist_id = gspoty.get_spotify_playlist_id(playlist_uri)
        print("Playlist {}".format(playlist_id))
        search_keys = gspoty.get_spotify_search_keys(playlist_id)
        print("Trying to create a new playlist with {} songs".format(len(search_keys)))
        gmusic_playlist = gspoty.build_gmusic_playlist(search_keys, playlist_id)
        print("List generated: {}".format(
            gspoty.get_shareable_link(gmusic_playlist)))
    except GspotyException as gs:
        print("Somenthing bad happend {}", gs)
        exit(4)
