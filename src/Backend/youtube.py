from .musicAppInterface import MusicAppInterface
from .song import Song
import numpy as np
from googleapiclient.discovery import build
import json
import re

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

api_key = data['youtube']['api_key']
client_id = data['youtube']['client_id']


class Youtube(MusicAppInterface):
    @staticmethod
    def playlist_to_array(playlist_link: str) -> np.ndarray:
        """convert playlist link to str ndarry of song names.

        Keyword arguments:
        playlist_link : str -- link to playlist

        return:
        np.ndarray[Song] -- array of songs
        """

        playlist_id = playlist_link.replace('https://youtube.com/playlist?list=', '')

        yt = build('youtube', 'v3', developerKey=api_key)  # public access approach, no user auth required

        # access the playlist and from it get to a list of songs id's, calls songs_requst,
        # which access the playlist songs by ids and save thier names (title)
        song_titles = Youtube.__playlist_request(yt, playlist_id)

        yt.close()

        # song title sometimes includes stuff like (lyrics) (offical Music Video) and such, shuld be cleaned out
        song_titles = Youtube.__clean_youtube_name_noise(song_titles)
        song_array = []
        for title in song_titles:
            # not taking artist name due to it usally being in the title / video uploded not by artist
            song_array.append(Song(title, ''))
        return np.array(song_array)

    @staticmethod
    def __playlist_request(yt: build, playlist_id: str) -> list[str]:
        """Take YouTube playlist and return list of song names.

        Keyword arguments:
        yt: build -- access to YouTube api
        playlist_id: str -- playlist id in YouTube format

        return:
        list[str] -- list of song names
        """

        next_page_token = 1
        song_titles = []
        # google requst can only send back a page of up to 50 results, so we loop over all the pages
        while next_page_token:
            if next_page_token == 1:  # for first loop next_page_token needs to be None
                next_page_token = None
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
            song_titles = Youtube.__songs_requst(yt, songs_ids, song_titles)
            next_page_token = pl_response.get('nextPageToken')
        return song_titles

    @staticmethod
    def __songs_requst(yt: build, song_ids: list[str], song_titles: list[str]) -> list[str]:
        """Access the playlist songs by ids and return thier names (title).

        Keyword arguments:
        yt: build -- access to YouTube api
        song_ids: list[str] -- song id's in YouTube format
        song_titles: list[str] -- list of song names to be added upon

        return:
        list[str] -- modified song_titles
        """

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
            # not taking channel name due to it usally being in the title / video uploded not by artist
        return song_titles

    @staticmethod
    def __clean_youtube_name_noise(songs_titles: list[str]) -> list[str]:
        """Clean song titles of noise that will disturb search functions. E.g.: (lyrics) (offical Music Video) and such.

        Keyword arguments:
        song_titles: list[str] -- list of song names to be cleaned

        return:
        list[str] -- modified song_titles
        """

        new_names = []
        for song_name in songs_titles:
            song_name = re.sub(r"(\(.*\))|(\[.*])|(\*.*\*)", "", song_name)
            song_name = re.sub(r'(?i:with lyrics|lyrics|video|offical|audio|hq|hd|studio|original|music|official|'
                               r'clip|promo|mp4|720p|1080p|full version|1280p|widescreen|version")', '', song_name)
            song_name = re.sub('\\s+', ' ', song_name)
            new_names.append(song_name)
        return new_names

    @staticmethod
    def array_to_playlist(song_list: np.ndarray, playlist_name: str) -> str:
        """convert ndarry of songs to a playlist.

        Keyword arguments:
        song_array: np.ndarray[Song] -- array of songs
        playlist_name: str -- name for new playlist

        return:
        str -- link to the newly created string
        """
        pass

    @staticmethod
    def search_song(song: Song, service_method) -> (bool, str):
        """searche a song on a specific platform.

        Keyword arguments:
        song: Song -- song to be searched
        service_method  -- open channel to a service (Spotify/YouTube/Apple Music)

        return:
        bool - True if search successful, False if not
        str -- song id if search successful, song name if not
        """
        pass
