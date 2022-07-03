import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from . import MusicAppInterface

client_id = '7a63f46f23384ee0a39460dcaa7b6272'
client_secret = 'b5979f8fda4d49a49e8315b4cf51ff64'
redirect_uri = 'https://open.spotify.com/collection/playlists' #'http://localhost:8501/callback'

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))


class Spotify(MusicAppInterface.MusicAppInterface):
    def __init__(self):
        super.__init__()

    """translate playlist link to string ndarry of song names"""
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        playlist = sp.playlist(playlist_link)
        songs_array = []
        for song in playlist['tracks']['items']:
            song_name = song['track']['name']
            artist = song['track']['artists'][0]['name']
            songs_array.append(MusicAppInterface.Song(song_name, artist))
        return np.array(songs_array)

    # input - Song, output - platform specific song
    @staticmethod
    def search_song(song: MusicAppInterface.Song)-> str:
        """searches for the song on spotify platform"""

        pass

    # input - string ndarry of songs, output - string PlaylistLink
    @staticmethod
    def array_to_playlist(song_list: np.ndarray, playlist_name: str):
        """translate ndarry of songs to playlist"""
        # create the playlist
        user_id = sp.me()['id']
        sp.user_playlist_create(user_id, playlist_name)
        user_playlists = sp.current_user_playlists()['items']
        for user_playlist in user_playlists:
            if user_playlist['name'] == playlist_name:
                new_playlist_id = user_playlist['id']
                break
        # add songs to the playlist
        track_list = []
        for song in song_list:
            track = Spotify.search_song(song)
            track_list.append(track)
        sp.playlist_add_items(new_playlist_id, track_list)


#
#
# playlist_link = 'https://open.spotify.com/playlist/37i9dQZF1DXdF699XuZIvg?si=02f0a763af604c95'
#
# songs_array = Spotify.playlist_to_array(playlist_link=playlist_link)
# for song in songs_array:
#     print(song.get_song_name() + ', ' + song.get_artist() + '\n')
# #user_id = sp.me()['id']
#sp.user_playlist_create(user_id, 'first playlist attempt')
