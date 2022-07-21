import streamlit as st
import playlistConverter
import numpy as np
from Backend.song import Song


def song_callback(song: Song):
    song.change_include()
    if song.get_is_include():
        st.session_state.songs_included += 1
    else:
        st.session_state.songs_included -= 1


def print_playlist_table(songs: np.ndarray, title: str):
    """Shows all the songs from the playlist on the screen, allows choice of what songs to move over.

    Keyword arguments:
    songs: np.ndarray[Song] -- playlist songs, to be presented
    title: str -- playlist title
    """

    playlist_table = st.expander('Expand:', True, )
    with playlist_table:
        title_culs = st.columns([1, 4])
        title_culs[0].subheader('{}/{}'.format(st.session_state.songs_included, songs.size))
        title_culs[1].subheader(title)
        i = 0
        for song in songs:
            columns = st.columns([1, 1, 7])
            columns[0].checkbox('', key=i, value=True, on_change=song_callback, args=(song,))
            columns[1].image(song.get_image(), width=40)
            columns[2].write(song.get_title() + ' ' + song.get_artist())
            st.write('')
            i += 1


st.title('platform playlist converter')

# set session arguments
if 'playlist_imported' not in st.session_state:
    st.session_state.playlist_imported = False
if 'song_array' not in st.session_state:
    st.session_state.song_array = np.ndarray
if 'playlist_title' not in st.session_state:
    st.session_state.playlist_title = ''
if 'playlist_link' not in st.session_state:
    st.session_state.playlist_link = ''
if 'songs_included' not in st.session_state:
    st.session_state.songs_included = 0

from_platform = st.selectbox(
    'Playlist from platform:',
    ('Spotify', 'YouTube'))  # 'Apple Music',

link = st.text_input('Playlist link:')

if link != st.session_state.playlist_link:  # The link was deleted or changed
    st.session_state.playlist_imported = False
    st.session_state.song_array = np.ndarray
    st.session_state.playlist_title = ''
    st.session_state.playlist_link = link

if st.session_state.playlist_link and not st.session_state.playlist_imported:
    try:
        st.session_state.song_array, st.session_state.playlist_title = \
            playlistConverter.link_to_array(from_platform=from_platform, playlist_link=link)
        st.session_state.playlist_imported = True
        st.session_state.songs_included = st.session_state.song_array.size
    except ValueError:
        st.write('playlist link invalid')

if st.session_state.playlist_imported:
    # present the playlist
    print_playlist_table(st.session_state.song_array, st.session_state.playlist_title)
    to_platform = st.selectbox(
        'Move to platform:',
        ('Spotify', 'YouTube'))  # 'Apple Music',

    playlist_name = st.text_input('Playlist name:', value=st.session_state.playlist_title)

    with st.empty():
        if st.button("Transform playlist"):
            with st.spinner('Moving playlist...'):
                transformed_playlist_data = playlistConverter.array_to_link(song_array=st.session_state.song_array,
                                                                            to_platform=to_platform,
                                                                            playlist_name=playlist_name)
            track_count = transformed_playlist_data['tracks_moved']+len(transformed_playlist_data['tracks_failed'])
            success_message = '{}/{} songs moved from {} to playlist "{}" on {}.\nNew playlist link: {}'\
                              .format(transformed_playlist_data['tracks_moved'], track_count, from_platform,
                                      playlist_name, to_platform, transformed_playlist_data['playlist_url'])
            st.success(success_message)
