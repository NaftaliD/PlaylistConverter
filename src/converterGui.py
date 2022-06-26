import streamlit as st
import playlistConverter


st.title('platform playlist converter')

fromPlatform = st.selectbox(
    'playlist from:',
    ('spotify', 'apple music', 'youtube'))

toPlatform = st.selectbox(
    'to:',
    ('spotify', 'apple music', 'youtube'))

link = st.text_input('playlist link')

if st.button("transform playlist"):
    st.write(type(fromPlatform), type(toPlatform), type(link))
    output_playlist = playlistConverter.convert_playlist(fromPlatform, toPlatform, link)
    st.write(output_playlist)
