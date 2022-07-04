from . import MusicAppInterface
import numpy as np
from googleapiclient.discovery import build
import json

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

api_key = data['youtube']['api_key']
client_id = data['youtube']['client_id']


class Youtube(MusicAppInterface.MusicAppInterface):
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """translate playlist link to string ndarry of song names"""
        playlist_id = playlist_link.replace('https://youtube.com/playlist?list=', '')

        yt = build('youtube', 'v3', developerKey=api_key)  # public access approach, no user auth required

        # access the playlist and from it get to a list of songs id's, calls songs_requst,
        # which access the playlist songs by ids and save thier names (title)
        song_titles = Youtube.playlist_requst(yt, playlist_id)

        yt.close()

        # song title sometimes includes stuff like (lyrics) (offical Music Video) and such, shuld be cleaned out
        song_titles = Youtube.clean_youtube_name_noise(song_titles)
        song_array = []
        for title in song_titles:
            # not taking artist name due to it usally being in the title / video uploded not by artist
            song_array.append(MusicAppInterface.Song(title, ''))

        return np.array(song_array)

    # acsses the playlist and from it get to a list of songs id's
    @staticmethod
    def playlist_requst(yt: build, playlist_id: str):
        next_page_token = None
        song_titles = []
        while True:  # google requst can only send back a page of up to 50 results, so we loop over all the pages
            pl_request = yt.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            pl_response = pl_request.execute()
            songs_ids = []
            for item in pl_response['items']:
                songs_ids.append(item['contentDetails']['videoId'])

            # acsses the playlist songs by ids and save thier names (title)
            song_titles = Youtube.songs_requst(yt, songs_ids, song_titles)
            next_page_token = pl_response.get('nextPageToken')
            if not next_page_token:
                break
        return song_titles

    # acsses the playlist songs by ids and save thier names (title)
    @staticmethod
    def songs_requst(yt: build, song_ids: list, song_titles: list):
        ids_string = ','.join(song_ids)
        vid_request = yt.videos().list(
            part='snippet',
            id=ids_string,
            maxResults=50,
        )
        vid_response = vid_request.execute()
        for item in vid_response['items']:
            song_name = item['snippet']['title']
            song_titles.append(song_name)
            # not taking artist name due to it usally being in the title / video uploded not by artist
        return song_titles

    # an attampt of cleaning noise from YouTube titles
    @staticmethod
    def clean_youtube_name_noise(songs_titles: list[str]):
        # TODO song title sometimes includes stuff like (lyrics) (offical Music Video) and such, it disturbs the
        #  search and shuld be cleaned, this function is a brute force sultion, sould improve upon it
        new_names = []
        for song_name in songs_titles:
            song_name = song_name.replace('Official Music Video', '')
            song_name = song_name.replace('Version Original', '')
            song_name = song_name.replace('Official Video', '')
            song_name = song_name.replace('official video', '')
            song_name = song_name.replace('With Lyrics', '')
            song_name = song_name.replace('With lyrics', '')
            song_name = song_name.replace('with lyrics', '')
            song_name = song_name.replace('Audio', '')
            song_name = song_name.replace('HQ', '')
            song_name = song_name.replace('HD', '')
            song_name = song_name.replace('Official Video Remastered', '')
            song_name = song_name.replace('Lyrics', '')
            song_name = song_name.replace('lyrics', '')
            song_name = song_name.replace('Video', '')
            song_name = song_name.replace('Studio Version', '')
            song_name = song_name.replace('(', '')
            song_name = song_name.replace(')', '')
            song_name = song_name.replace(']', '')
            song_name = song_name.replace('[', '')

            new_names.append(song_name)
        return new_names
        pass

    # input - string ndarry of songs, output - string PlaylistLink
    @staticmethod
    def array_to_playlist(song_list: np.ndarray, playlist_name: str) -> str:
        """translate string ndarry of song names to playlist link"""
        pass

    # input - Song, output - platform specific song
    @staticmethod
    def search_song(song: MusicAppInterface.Song, service_method) -> str:
        """searches for the song on the specific platform"""
        pass
