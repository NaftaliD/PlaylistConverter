import streamlit as st
import playlistConverter


st.title('platform playlist converter')

from_platform = st.selectbox(
    'Playlist from platform:',
    ('Spotify', 'Apple Music', 'YouTube'))

link = st.text_input('Playlist link:')

to_platform = st.selectbox(
    'Move to platform:',
    ('Spotify', 'Apple Music', 'YouTube'))

playlist_name = st.text_input('Playlist name:')

if st.button("Transform playlist"):
    playlistConverter.convert_playlist(from_platform, to_platform, link, playlist_name)
