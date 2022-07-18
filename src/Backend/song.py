class Song:
    __title = ''
    __artist = ''
    __image = None

    def __init__(self, title: str, artist: str, image=None):
        self.__artist = artist
        self.__title = title
        self.__image = image

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
