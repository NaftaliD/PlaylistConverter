import streamlit as st
import playlistConverter


st.title('platform playlist converter')

fromPlatform = st.selectbox(
    'Playlist from platform:',
    ('Spotify', 'Apple Music', 'YouTube'))

link = st.text_input('Playlist link:')

toPlatform = st.selectbox(
    'Move to platform:',
    ('Spotify', 'Apple Music', 'YouTube'))

playlist_name = st.text_input('Playlist name:')

if st.button("Transform playlist"):
    playlistConverter.convert_playlist(fromPlatform, toPlatform, link, playlist_name)
