import streamlit as st
import playlistConverter


st.title('platform playlist converter')

fromPlatform = st.selectbox(
    'playlist from platform:',
    ('spotify', 'apple music', 'youtube'))

link = st.text_input('playlist link:')

toPlatform = st.selectbox(
    'move to platform:',
    ('spotify', 'apple music', 'youtube'))

playlist_name = st.text_input('playlist name:')

if st.button("transform playlist"):
    playlistConverter.convert_playlist(fromPlatform, toPlatform, link, playlist_name)
