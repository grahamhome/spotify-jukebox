from time import sleep

from dotenv import load_dotenv

from lifx_control import LifxSwitch
from spotify_client import SpotifyClient


class Jukebox:

    def __init__(self):
        self.spotify_client = SpotifyClient()
        self.lifx_switch = LifxSwitch()

    def play(self):
        prev_track = None
        while True:
            self.spotify_client.wait_for_login()
            track = self.spotify_client.now_playing()
            if track and track.get("id") != prev_track:
                self.lifx_switch.set_scene(track["album_art_colors"])
                prev_track = track.get("id")
            sleep(3)

def main():
    load_dotenv()
    Jukebox().play()


if __name__ == "__main__":
    main()
