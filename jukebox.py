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
        accumulator = 0
        while True:
            self.spotify_client.wait_for_login()
            track = self.spotify_client.now_playing()
            if track and (track.get("id") != prev_track or accumulator == 2):
                self.lifx_switch.get_lights(randrange(2, 4))
                self.lifx_switch.set_scene(track["album_art_colors"])
                prev_track = track.get("id")
                accumulator = 0
            accumulator += 1
            sleep(3)

def main():
    load_dotenv()
    jukebox = Jukebox()
    jb_thread = Thread(target=jukebox.play)
    jb_thread.start()
    auth_app_main()


if __name__ == "__main__":
    main()
