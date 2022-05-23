import streamlit as st
import pandas as pd
import numpy as np

st.title('platform playlist converter')

fromPlatform = st.selectbox(
    'playlist from:',
    ('spotify', 'apple music', 'youtube'))

toPlatform = st.selectbox(
    'to:',
    ('spotify', 'apple music', 'youtube'))

Link = st.text_input('playlist link')

if st.button("transform playlist"):
    pass #should call convertplaylist from src convertPlaylist.py