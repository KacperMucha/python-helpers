"""
The script assumes following environment variables exitence:
SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI

It's meant for finding a track in my Spotify saved playlists.
This feature is not available in the Spotify app.
"""

import sys
import json
import spotipy
import spotipy.util as util

if len(sys.argv) > 1:
    username = sys.argv[1]
    track_name = sys.argv[2]
else:
    print("Usage: %s username track_name" % (sys.argv[0],))
    sys.exit()

scope = ''
token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    playlist_offset = 0
    all_playlists = list()
    current_playlists = sp.current_user_playlists(limit=50)
    while current_playlists['next']:
        playlist_offset += 50
        all_playlists += current_playlists['items']
        current_playlists = sp.current_user_playlists(limit=50, offset=playlist_offset)
    else:
        all_playlists += current_playlists['items']

    result = list()
    i = 1
    for playlist in all_playlists:
        print(f"Processing playlist {i} out of {len(all_playlists)}")
        i += 1

        playlist = sp.playlist(playlist['id'])
        all_tracks = list(playlist['tracks']['items'])

        for track in all_tracks:
            try:
                if track['track'] is not None:
                    if track_name.lower() in track['track']['name'].lower():
                        result += [f"Found track in playlist {playlist['name']}"]
            except ValueError as e:
                print(f"Error details: ${e}")

    for r in result:
        print(r)
else:
    print("Can't get token for", username)