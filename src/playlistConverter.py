import numpy as np
from Backend import appleMusic, spotify, youtube


def convert_playlist(from_platform: str, to_platform: str, playlist_link: str,
                     playlist_name='New converted playlist!') -> str:
    """Convert playlist from one platform to another.

    Keyword arguments:
    from_platform: str -- The platform the playlist is from
    to_platform: str -- The platform for the output playlist
    playlist_link: str -- Link to the original playlist
    playlist_name: str -- New playlist name ('New converted playlist!')

    return:
    str -- link to playlist on the new platform
    """

    # input check
    if type(from_platform) != type(to_platform) != type(playlist_link) != type(playlist_name)\
            or type(from_platform) != str:
        raise TypeError('Wrong input type, convert_playlist should only get strings.')
    if not(from_platform == 'Spotify' or from_platform == 'Apple Music' or from_platform == 'YouTube'):
        raise ValueError('From_platform must be one of: Spotify, Apple Music, YouTube.')
    if not(to_platform == 'Spotify' or to_platform == 'Apple Music' or to_platform == 'YouTube'):
        raise ValueError('to_platform must be one of: Spotify, Apple Music, YouTube.')

    # Turn the playlist link into an array of song names to be used later
    song_array = link_to_array(from_platform=from_platform, playlist_link=playlist_link)
    # Turn the array of songs to a playlist on the required platform
    output_playlist = array_to_link(song_array, to_platform=to_platform, playlist_name=playlist_name)

    return output_playlist


# Turn the playlist link into an array of song names to be used later
def link_to_array(from_platform: str, playlist_link: str) -> np.ndarray:
    """Convert playlist link to np.ndarray of songs.

    Keyword arguments:
    from_platform: str -- The platform the playlist is from
    playlist_link: str -- Link to the original playlist

    return:
    np.ndarray[Song] -- array of songs
    """

    if from_platform == 'Spotify':
        song_array = spotify.Spotify.playlist_to_array(playlist_link)
    elif from_platform == 'Apple Music':
        # song_array = appleMusic.playlist_to_array(playlist_link)
        song_array = []
    elif from_platform == 'YouTube':
        song_array = youtube.Youtube.playlist_to_array(playlist_link)
    else:
        raise ValueError('From_platform must be one of: Spotify, Apple Music, YouTube.')
    return song_array


def array_to_link(song_array: np.ndarray, to_platform: str, playlist_name: str) -> str:
    """Convert array of songs to a playlist.

    Keyword arguments:
    song_array: np.ndarray[Song] -- array of songs
    to_platform: str -- The platform for the output playlist
    playlist_name: str -- New playlist name

    return:
    str -- link to playlist on the new platform
    """

    if to_platform == 'Spotify':
        output_playlist = spotify.Spotify.array_to_playlist(song_array, playlist_name)
    elif to_platform == 'Apple Music':
        # output_playlist = appleMusic.array_to_playlist(song_array)
        output_playlist = 'place holder'
        pass
    elif to_platform == 'YouTube':
        # output_playlist = youtube.array_to_playlist(song_array)
        output_playlist = 'place holder'
        pass
    else:
        raise ValueError('to_platform must be one of: Spotify, Apple Music, YouTube.')
    return output_playlist
