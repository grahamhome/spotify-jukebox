from typing import List
from pprint import pprint

from gcloud_control import GoogleVision

class Song:
    """
    Contains details about a song.
    """
    vision = GoogleVision()

    def __init__(self):
        self.spotify_id = None
        self.title = None
        self.artists = []
        self.album = None
        self.album_art = None
        self.album_art_colors = []
        self.lyrics = None
        self.paused = False

    async def update(self, spotify_id: str, title: str, artists: List[str], album: str, album_art: str, lyrics: str):
        """
        Update fields with new values.
        :param spotify_id:
        :param title:
        :param artists:
        :param album:
        :param album_art:
        :param lyrics:
        :return:
        """
        self.spotify_id = spotify_id
        self.title = title
        self.artists[:] = artists
        self.album = album
        self.album_art = album_art
        self.lyrics = lyrics
        self.album_art_colors = await self.vision.get_image_colors(album_art)
