import numpy as np
import requests.exceptions
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import json
from .musicAppInterface import MusicAppInterface
from .song import Song

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

CLIENT_ID = data['Spotify']['client_id']
CLIENT_SECRET = data['Spotify']['client_secret']
REDIRECT_URL = data['Spotify']['redirect_url']
SPOTIFY_SCOPE = data['Spotify']['scope']
SPOTIFY_MAX_TRACKS_TO_ADD_AT_ONCE = int(data['Spotify']['spotify_max_tracks_to_add_at_once'])


class Spotify(MusicAppInterface):
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """convert playlist link to str ndarry of song names.

        Keyword arguments:
        playlist_link : str -- link to playlist

        return:
        np.ndarray[Song] -- array of songs
        """

        # open a spotify instance, using client Credentials, no user auth required
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                                                 client_secret=CLIENT_SECRET))
        # read playlist
        try:
            playlist = sp.playlist(playlist_link)
        except (requests.exceptions.HTTPError, spotipy.exceptions.SpotifyException):
            raise ValueError('invalid spotify playlist link')
        songs_array = []
        for song in playlist['tracks']['items']:
            song_name = song['track']['name']
            artist = song['track']['artists'][0]['name']
            songs_array.append(Song(song_name, artist))
        return np.array(songs_array)

    @staticmethod
    def array_to_playlist(song_array: np.ndarray, playlist_name: str) -> str:
        """convert np.ndarray of songs to a playlist.

        Keyword arguments:
        song_array: np.ndarray[Song] -- array of songs
        playlist_name: str -- name for new playlist

        return:
        str -- link to the newly created string
        """

        # check inputs
        if type(playlist_name) != str or type(song_array) != np.ndarray:
            raise TypeError('array_to_playlist shuld recieve an np.ndarray and a string')
        if playlist_name == '' or not song_array.size:
            raise ValueError('array_to_playlist inputs cant be empty')
        # open a spotify instance, using auth manager, user auth required
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=REDIRECT_URL,
                                                       scope=SPOTIFY_SCOPE))
        # create the playlist
        user_id = sp.me()['id']
        new_playlist = sp.user_playlist_create(user_id, playlist_name)
        # add songs to the playlist
        Spotify.__playlist_add_tracks(new_playlist['id'], song_array=song_array, sp=sp)
        return new_playlist['external_urls']['spotify']

    @staticmethod
    def __playlist_add_tracks(playlist_id: str, song_array: np.ndarray, sp: spotipy):
        """searche a song on a specific platform.

        Keyword arguments:
        playlist_id: str -- spotify id of a playlist
        song_array: np.ndarray[Song] -- array of songs
        sp: spotipy  -- open channel to a service (Spotify/YouTube/Apple Music)
        """

        track_list = []  # list off all the tracks to add, holds track_ids
        for song in song_array:
            did_find_song, track = Spotify.__search_song(song, sp)
            if did_find_song:
                track_list.append(track)
        if len(track_list):
            for i in range(0, len(track_list), SPOTIFY_MAX_TRACKS_TO_ADD_AT_ONCE):
                sp.playlist_add_items(playlist_id, track_list[i:i + SPOTIFY_MAX_TRACKS_TO_ADD_AT_ONCE])

    @staticmethod
    def __search_song(song: Song, sp: spotipy) -> (bool, str):
        """searche a song on a specific platform.

        Keyword arguments:
        song: Song -- song to be searched
        sp:spotify  -- open channel to a service (Spotify/YouTube/Apple Music)

        return:
        bool - True if search successful, False if not
        str -- song id if search successful, song name if not
        """
        # check input
        if not song.get_song_name() or type(song.get_artist()) is not str or song.get_song_name() == '':
            raise ValueError('search_song input song must contain a name')
        quary = song.get_song_name() + ' ' + song.get_artist()
        result = sp.search(q=quary, limit=1, type='track')
        if len(result['tracks']['items']):
            return True, result['tracks']['items'][0]['id']
        else:  # search failed on spotify
            return False, quary
