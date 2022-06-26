SPOTIPY_CLIENT_ID = '7a63f46f23384ee0a39460dcaa7b6272'
SPOTIPY_CLIENT_SECRET = 'b5979f8fda4d49a49e8315b4cf51ff64'
SPOTIPY_REDIRECT_URI = 'http://localhost:8501/'

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= SPOTIPY_CLIENT_ID, client_secret= SPOTIPY_CLIENT_SECRET, redirect_uri= SPOTIPY_REDIRECT_URI,scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])