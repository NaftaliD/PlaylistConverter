class Song:
    __song_name = ''
    __artist = ''
    __image = None

    def __init__(self, song_name: str, artist: str, image=None):
        self.__artist = artist
        self.__song_name = song_name
        self.__image = image

    def get_artist(self) -> str:
        """get song's artist"""
        return self.__artist

    def get_song_name(self) -> str:
        """get song's name"""
        return self.__song_name

    def get_song_image(self) -> str:
        """get song's image"""
        return self.__image
