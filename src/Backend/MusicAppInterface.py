import numpy as np


class Song:
    __song_name = ''
    __artist = ''

    def __init__(self, song_name: str, artist: str):
        self.__artist = artist
        self.__song_name = song_name

    def get_artist(self) -> str:
        """get song's artist"""
        return self.__artist

    def get_song_name(self) -> str:
        """get song's name"""
        return self.__song_name


class MusicAppInterface:
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """convert playlist link to str ndarry of song names.

        Keyword arguments:
        playlist_link : str -- link to playlist

        return:
        np.ndarray[Song] -- array of songs
        """

        pass

    @staticmethod
    def array_to_playlist(song_array: np.ndarray, playlist_name: str) -> str:
        """convert ndarry of songs to a playlist.

        Keyword arguments:
        song_array: np.ndarray[Song] -- array of songs
        playlist_name: str -- name for new playlist

        return:
        str -- link to the newly created string
        """

        pass

    @staticmethod
    def search_song(song: Song, service_method) -> (bool, str):
        """searche a song on a specific platform.

        Keyword arguments:
        song: Song -- song to be searched
        service_method  -- open channel to a service (Spotify/YouTube/Apple Music)

        return:
        bool - True if search successful, False if not
        str -- song id if search successful, song name if not
        """

        pass
