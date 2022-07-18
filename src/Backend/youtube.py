from .musicAppInterface import MusicAppInterface
from .song import Song
import numpy as np
from googleapiclient.discovery import build
import json
import re
from . import youtubeOAuth

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

API_KEY = data['YouTube']['api_key']
CLIENT_ID = data['YouTube']['client_id']
YOUTUBE_SCOPE = data['YouTube']['scope']
YOUTUBE_URL = data['YouTube']['url']


class Youtube(MusicAppInterface):
    @staticmethod
    def playlist_to_array(playlist_link: str) -> (np.ndarray, str):
        """convert playlist link to str ndarry of song names.

        Keyword arguments:
        playlist_link : str -- link to playlist

        return:
        np.ndarray[Song] -- array of songs
        str -- playlist_title
        """

        playlist_id = playlist_link.replace(YOUTUBE_URL, '')

        # TODO add checks for playlist link validity

        yt = build('youtube', 'v3', developerKey=API_KEY)  # public access approach, no user auth required

        # access the playlist and from it get to a list of songs id's, calls songs_requst,
        # which access the playlist songs by ids and save thier names (title)
        song_titles = Youtube.__playlist_request(yt, playlist_id)
        playlist_title = ''  # TODO implement this
        yt.close()

        # song title sometimes includes stuff like (lyrics) (offical Music Video) and such, shuld be cleaned out
        song_titles = Youtube.__clean_youtube_name_noise(song_titles)
        song_array = []
        for title in song_titles:
            # not taking artist name due to it usally being in the title / video uploded not by artist
            song_array.append(Song(title, ''))
        return np.array(song_array), playlist_title

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
    def array_to_playlist(song_array: np.ndarray, playlist_name: str) -> str:
        """Convert ndarry of songs to a playlist.

        Keyword arguments:
        song_array: np.ndarray[Song] -- array of songs
        playlist_name: str -- name for new playlist

        return:
        str -- link to the newly created string
        """

        credentials = youtubeOAuth.handle_oauth(YOUTUBE_SCOPE)
        yt = build('youtube', 'v3', credentials=credentials)  # private access approach, user OAuth2.0 required

        pl_request = yt.playlists().insert(part="snippet, status", body={"snippet": {"title": playlist_name},
                                                                         "status": {"privacyStatus": "public"}})
        pl_response = pl_request.execute()  # create the playlist
        playlist_id = pl_response['id']

        # Add song to the playlist
        for song in song_array:
            song_found, song_id = Youtube.__search_song(song, yt)
            if song_found:
                song_request = yt.playlistItems().insert(part="snippet",
                                                         body={"snippet": {"playlistId": playlist_id,
                                                                           "resourceId": {"kind": "youtube#video",
                                                                                          "videoId": song_id}}})
                song_request.execute()
        return YOUTUBE_URL + playlist_id

    @staticmethod
    def __search_song(song: Song, yt) -> (bool, str):
        """searche a song on a specific platform.

        Keyword arguments:
        song: Song -- song to be searched
        service_method, yt: build  -- open channel to a service (Spotify/YouTube/Apple Music)

        return:
        bool - True if search successful, False if not
        str -- song id if search successful, song name if not
        """
        # check input
        if not song.get_song_name() or not song.get_artist() or song.get_song_name() == '':
            raise ValueError('search_song input song must contain a name')

        quary = song.get_song_name() + ' ' + song.get_artist()
        search_request = yt.search().list(part="snippet", maxResults=1, q=quary, type="video")
        search_response = search_request.execute()
        if search_response['pageInfo']['totalResults']:
            return True, search_response['items'][0]['id']['videoId']
        else:  # search failed on YouTube
            return False, quary
