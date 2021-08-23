from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    """
    Contains details about a song.
    """
    spotify_id: str
    title: str
    artists: List[str]
    album: str
    album_art: str
    lyrics: str


class NowPlaying:
    """
    Singleton class representing the currently-playing song.
    """

    instance = None

    def __init__(self):
        self.song = None

    @staticmethod
    def get():
        if not NowPlaying.instance:
            NowPlaying.instance = NowPlaying()
        return NowPlaying.instance
