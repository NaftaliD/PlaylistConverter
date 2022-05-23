import numpy as np


class MusicAppInterface:
    # input - string PlaylistLink, output - string ndarry of songs
    def playlist_to_array(self, playlist_link: str) -> np.ndarray:
        """translate playlist link to string ndarry of song names"""
        pass

    # input - string ndarry of songs, output - string PlaylistLink
    def array_to_playlist(self, song_list: np.ndarray) -> str:
        """translate string ndarry of song names to playlist link"""
        pass
