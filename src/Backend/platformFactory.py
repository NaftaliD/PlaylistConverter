import platform
from typing import Type
from enum import Enum
from Backend.musicAppInterface import MusicAppInterface
from Backend import appleMusic, spotify, youtube

class MusicPlatform(Enum):
    Spotify = 'Spotify'
    Youtube = 'Youtube'
    AppleMusic = 'Apple Music'
    
    @staticmethod
    def isValue(platform: str):
        return platform in platform in MusicPlatform._value2member_map_.keys()

class PlatformFactory:
    @staticmethod
    def getPlatform(platform: MusicPlatform) -> Type[MusicAppInterface]:
        """Get Platform class by string

        Args:
            platform (PLATFORM): The platform to retrieve: Spotify, Youtube, or Apple Music

        Raises:
            ValueError: Platform must be one of: Spotify, Apple Music, YouTube.

        Returns:
            Type[MusicAppInterface]: The platform specific implementation
        """
        if not MusicPlatform.isValue(platform):
            raise ValueError('Platform must be of type string and one of: Spotify, Apple Music, YouTube.')
        
        match platform:
            case 'Spotify':
                return spotify.Spotify
            case 'Youtube':
                return youtube.Youtube
            # case 'Apple Music':
            #     return appleMusic.AppleMusic
            case _:
                raise ValueError("platform: " + platform + " is unsupported");