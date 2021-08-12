from random import randrange
from time import sleep

from dotenv import load_dotenv

from lifx_control import LifxSwitch
from spotify_client import SpotifyClient
from spotify_auth_callback_handler import main as auth_app_main
from threading import Thread


class Jukebox:

    def __init__(self):
        self.spotify_client = SpotifyClient()
        self.lifx_switch = LifxSwitch()

    def play(self):
        prev_track = None
        while True:
            self.spotify_client.wait_for_login()
            track = self.spotify_client.now_playing()
            if track and (track.get("id") != prev_track):
                self.lifx_switch.set_scene_pulse(track["album_art_colors"])
                self.lifx_switch.get_lights(randrange(2, 4))
                prev_track = track.get("id")
            sleep(3)

def start_jukebox():
    # Allow time for auth app to start in other process
    sleep(3)
    Jukebox().play()

def main():
    load_dotenv()
    jb_thread = Thread(target=start_jukebox())
    jb_thread.start()
    auth_app_main()


if __name__ == "__main__":
    main()
