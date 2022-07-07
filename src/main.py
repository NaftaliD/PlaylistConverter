import playlistConverter

spotify_playlist = 'https://open.spotify.com/playlist/37i9dQZF1DXdF699XuZIvg?si=02f0a763af604c95'
youtube_playlist = 'https://youtube.com/playlist?list=PLNxOe-buLm6cz8UQ-hyG1nm3RTNBUBv3K'


new_playlist_id = playlistConverter.convert_playlist(from_platform='Spotify',
                                                     to_platform='YouTube',
                                                     playlist_link=spotify_playlist,
                                                     playlist_name='Playlist attempt')
print('Playlist converted, new playlist link: ' + new_playlist_id)
