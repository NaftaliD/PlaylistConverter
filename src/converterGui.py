import streamlit as st
import playlistConverter
import numpy as np


def checkbox_callback(songs_set: set, key):
    songs_set.add(key)


def print_playlist_table(songs: np.ndarray, title: str) -> set:
    playlist_table = st.expander('Expand:', True, )
    songs_not_to_transform = set()
    with playlist_table:
        title_culs = st.columns([1, 5, 1])
        title_culs[1].header(title)
        i = 0
        for song in songs:
            columns = st.columns([1, 1, 7])
            columns[0].checkbox('', key=i, value=True, on_change=checkbox_callback, args=(songs_not_to_transform, i))
            columns[1].image(song.get_image(), width=40)
            columns[2].write(song.get_title() + ' ' + song.get_artist())
            st.write('')
            i += 1
    return songs_not_to_transform


st.title('platform playlist converter')

from_platform = st.selectbox(
    'Playlist from platform:',
    ('Spotify', 'YouTube'))  # 'Apple Music',

link = st.text_input('Playlist link:')

playlist_title = ''
song_array = []
if link:
    try:
        song_array, playlist_title = playlistConverter.link_to_array(from_platform=from_platform, playlist_link=link)
    except ValueError:
        st.write('playlist link invalid')

if playlist_title:
    # present the playlist
    print_playlist_table(song_array, playlist_title)
    to_platform = st.selectbox(
        'Move to platform:',
        ('Spotify', 'YouTube'))  # 'Apple Music',

    playlist_name = st.text_input('Playlist name:', value=playlist_title)

    if st.button("Transform playlist"):
        tranformed_playlist_link = playlistConverter.array_to_link(song_array=song_array, to_platform=to_platform,
                                                                   playlist_name=playlist_name)
        st.success('Playlist converted to ' + to_platform + ', new playlist link: ' + tranformed_playlist_link)
