import streamlit as st
import playlistConverter
import pandas as pd


st.title('platform playlist converter')

from_platform = st.selectbox(
    'Playlist from platform:',
    ('Spotify', 'Apple Music', 'YouTube'))

link = st.text_input('Playlist link:')

playlist_title = ''
if link:
    try:
        song_array, playlist_title = playlistConverter.link_to_array(from_platform=from_platform, playlist_link=link)
    except ValueError:
        st.write('playlist link invalid')

if playlist_title:
    # present the playlist
    playlist_table = st.expander('Expand:', True,)
    songs_not_to_transform = set()

    def checkbox_callback(songs_set: set, key):
        songs_set.add(key)
    with playlist_table:
        title_culs = st.columns([1, 2, 1])
        title_culs[1].header(playlist_title)
        i = 0
        for song in song_array:
            columns = st.columns([1, 1, 7])
            columns[0].checkbox('', key=i, value=True, on_change=checkbox_callback, args=(songs_not_to_transform, i))
            columns[1].image(song.get_song_image(), width=35)
            columns[2].write(song.get_song_name() + ' ' + song.get_artist())
            st.write('')
            i += 1
    # playlist_songs = []
    # for song in song_array:
    #     playlist_songs.append({'picture': song.get_song_image(),
    #                            'song name': song.get_song_name() + ' ' + song.get_artist()})
    # playlist_songs = pd.DataFrame(playlist_songs)
    # st.beta_columns()
    # st.dataframe(pd.DataFrame(playlist_songs))

    to_platform = st.selectbox(
        'Move to platform:',
        ('Spotify', 'Apple Music', 'YouTube'))

    playlist_name = st.text_input('Playlist name:', value=playlist_title)
    if st.button("Transform playlist"):
        tranformed_playlist_link = playlistConverter.array_to_link(song_array=song_array, to_platform=to_platform,
                                                                   playlist_name=playlist_name)
        st.write('Playlist converted to ' + to_platform + ', new playlist link: ' + tranformed_playlist_link)
