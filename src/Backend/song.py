class Song:
    __title = ''
    __artist = ''
    __image = ''
    __include = True

    def __init__(self, title: str, artist='', image=''):
        """create a Song object

        Keyword arguments:
        title: str -- mandatory, Title of the song
        artist: str -- optional, The song's artist
        image: str -- optional, Image of the song/album

        return:
        Song -- Song object
        """
        self.__artist = artist
        self.__title = title
        self.__image = image
        self.__include = True

    def get_artist(self) -> str:
        """get song's artist"""
        return self.__artist

    def get_title(self) -> str:
        """get song's name"""
        return self.__title

    def set_title(self, title: str):
        """set song title"""
        self.__title = title

    def get_image(self) -> str:
        """get song's image"""
        return self.__image

    def get_is_include(self) -> bool:
        """get song's include boolean"""
        return self.__include

    def change_include(self):
        """"change the include option of the song"""
        self.__include = not self.__include
