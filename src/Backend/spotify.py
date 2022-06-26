import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import MusicAppInterface

client_id = '7a63f46f23384ee0a39460dcaa7b6272'
client_secret = 'b5979f8fda4d49a49e8315b4cf51ff64'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class Spotify(MusicAppInterface.MusicAppInterface):
    """translate playlist link to string ndarry of song names"""
    def __init__(self):
        super.__init__()

    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        playlist = sp.playlist(playlist_link)
        songs_array = []
        artist = ''
        song_name = ''
        for song in playlist['tracks']['items']:
            song_name = song['track']['name']
            artist = song['track']['artists'][0]['name']
            songs_array.append(MusicAppInterface.Song(song_name, artist))
        return np.array(songs_array)

    # input - string ndarry of songs, output - string PlaylistLink
    def array_to_playlist(self, song_list: np.ndarray, playlist_name: str) -> str:
        """translate string ndarry of song names to playlist link"""

        pass


playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXdF699XuZIvg?si=02f0a763af604c95'

songs_array = Spotify.playlist_to_array(playlist_link=playlist_link)
for song in songs_array:
    print(song.get_song_name() + ', ' + song.get_artist() + '\n')
#user_id = sp.me()['id']
#sp.user_playlist_create(user_id, 'first playlist attempt')
