from typing import Type
from enum import Enum
from .musicAppInterface import MusicAppInterface
from . import appleMusic, spotify, youtube


class MusicPlatform(Enum):
    Spotify = 'Spotify'
    YouTube = 'YouTube'
    AppleMusic = 'Apple Music'
    
    @staticmethod
    def is_value(platform: str):
        for enum in MusicPlatform:
            if platform is enum.value:
                return True
        return False


class PlatformFactory:
    @staticmethod
    def get_platform(platform: str) -> Type[MusicAppInterface]:
        """Get Platform class by string

        Args:
            platform (PLATFORM): The platform to retrieve: Spotify, YouTube, or Apple Music

        Raises:
            ValueError: Platform must be one of: Spotify, Apple Music, YouTube.

        Returns:
            Type[MusicAppInterface]: The platform specific implementation
        """

        if not MusicPlatform.is_value(platform):
            raise ValueError('Platform must be of type string and one of: Spotify, Apple Music, YouTube.')

        if platform == 'Spotify':
            return spotify.Spotify
        elif platform == 'YouTube':
            return youtube.Youtube
        elif platform == 'Apple Music':
            raise ValueError('Apple Music isnt implemented yet')
            return appleMusic.AppleMusic
        else:
            raise ValueError("platform: " + platform + " is unsupported")

        # better approach to do this function but only implemented in py3.10
        # match platform:
        #     case 'Spotify':
        #         return spotify.Spotify
        #     case 'Youtube':
        #         return youtube.Youtube
        #     # case 'Apple Music':
        #     #     return appleMusic.AppleMusic
        #     case _:
        #         raise ValueError("platform: " + platform + " is unsupported");
