import os
from time import sleep

import spotipy
from dotenv import load_dotenv

from gcloud_control import get_image_colors
from lifx_control import LifxSwitch
from spotify_auth_callback_handler import cache_path


class Jukebox:

    def __init__(self):

        self.cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
        self.auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing',
                                                   cache_handler=self.cache_handler,
                                                   show_dialog=True)
        self.wait_for_login()
        self.spotify_client = spotipy.Spotify(auth_manager=self.auth_manager)

        self.greeting = f"Welcome, {self.spotify_client.me().get('display_name')}!"
        self.lifx_switch = LifxSwitch()



    def wait_for_login(self):
        if not self.auth_manager.validate_token(self.cache_handler.get_cached_token()):
            # Display sign in link when no token
            auth_url = self.auth_manager.get_authorize_url()
            print(f"Please login: {auth_url}")
            while not self.auth_manager.validate_token(self.cache_handler.get_cached_token()):
                sleep(1)
            print(self.greeting)

    def play(self):

        last_track = {}
        print(self.greeting)
        while True:
            self.wait_for_login()
            track = self.spotify_client.current_user_playing_track()
            if track:
                if track.get("item").get("id") != last_track.get("id"):
                    last_track["id"] = track.get("item").get("id")
                    last_track["title"] = track.get("item").get("name")
                    last_track["artists"] = [artist.get("name") for artist in track.get("item").get("artists")]
                    last_track["album"] = track.get("item").get("album").get("name")
                    last_track["album_art"] = track.get("item").get("album").get("images")[0].get("url")
                    last_track["album_art_colors"] = get_image_colors(last_track["album_art"])

                    self.lifx_switch.set_scene(last_track["album_art_colors"])
            sleep(3)

def main():
    load_dotenv()
    Jukebox().play()


if __name__ == "__main__":
    main()
