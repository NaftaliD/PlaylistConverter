import numpy as np


class Song:
    song_name = ''
    artist = ''

    def __init__(self, song_name: str, artist: str):
        self.artist = artist
        self.song_name = song_name

    def get_artist(self):
        return self.artist

    def get_song_name(self):
        return self.song_name


class MusicAppInterface:
    # input - string PlaylistLink, output - string ndarry of songs
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """translate playlist link to string ndarry of song names"""
        pass

    # input - string ndarry of songs, output - string PlaylistLink
    @staticmethod
    def array_to_playlist(song_list: np.ndarray, playlist_name: str) -> str:
        """translate string ndarry of song names to playlist link"""
        pass

    # input - Song, output - platform specific song
    @staticmethod
    def search_song(song: Song, service_method) -> str:
        """searches for the song on the specific platform"""
        pass

