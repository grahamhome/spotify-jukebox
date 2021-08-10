from copy import deepcopy
from time import sleep

import spotipy

from gcloud_control import get_image_colors
from spotify_auth_callback_handler import cache_path


class SpotifyClient:

    def __init__(self):
        self.cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing',
                                                        cache_handler=self.cache_handler,
                                                        show_dialog=True)
        self.client = spotipy.Spotify(auth_manager=self.auth_manager)
        self.wait_for_login()
        self.greeting = f"Welcome, {self.client.me().get('display_name')}!"
        self.current_track = {}

    def wait_for_login(self):
        if not self.auth_manager.validate_token(self.cache_handler.get_cached_token()):
            # Display sign in link when no token
            auth_url = self.auth_manager.get_authorize_url()
            print(f"Please login: {auth_url}")
            while not self.auth_manager.validate_token(self.cache_handler.get_cached_token()):
                sleep(1)
            print(self.greeting)

    def now_playing(self):
        track = self.client.current_user_playing_track()
        if track:
            if  track.get("item").get("id") != self.current_track.get("id"):
                self.current_track["id"] = track.get("item").get("id")
                self.current_track["title"] = track.get("item").get("name")
                self.current_track["artists"] = [artist.get("name") for artist in track.get("item").get("artists")]
                self.current_track["album"] = track.get("item").get("album").get("name")
                self.current_track["album_art"] = track.get("item").get("album").get("images")[0].get("url")
                self.current_track["album_art_colors"] = get_image_colors(self.current_track["album_art"])
        return self.current_track
