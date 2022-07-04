import numpy as np


class Song:
    __song_name = ''
    __artist = ''

    def __init__(self, song_name: str, artist: str):
        self.__artist = artist
        self.__song_name = song_name

    def get_artist(self):
        return self.__artist

    def get_song_name(self):
        return self.__song_name


class MusicAppInterface:
    # input - string PlaylistLink, output - string ndarry of songs
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """translate playlist link to string ndarry of song names

        Parameters
        ----------
        playlist_link : str
            link of a playlist to be transformed

        Returns
        -------
        np.ndarray[Song]
            array of songs in the Song class format
        """
        pass

    # input - string ndarry of songs, output - string PlaylistLink
    @staticmethod
    def array_to_playlist(song_list: np.ndarray, playlist_name: str) -> str:
        """

        Args:
            song_list: np.ndarray[Song]
                array of songs
            playlist_name: str
                name for the new playlist

        Returns:
            str:
                link to the newly created playlist
        """
        pass

    # input - Song, output - platform specific song
    @staticmethod
    def search_song(song: Song, service_method) -> str:
        """searches for the song on the specific platform"""
        pass

