import tekore as tk
from pprint import pprint
import asyncio
from dotenv import load_dotenv
import os

class Spotify:
    """
    Interface to the Spotify API
    """
    token_file = "spotify_token.tok"

    def __init__(self, now_playing):
        load_dotenv()
        self.config = tk.config_from_environment()
        self.creds = tk.Credentials(*self.config)
        self.auth = tk.UserAuth(self.creds, tk.scope.user_read_currently_playing)
        self.client = tk.Spotify(asynchronous=True)
        self.now_playing = now_playing
        self.retrieve_token()

    def auth_url(self):
        """
        Returns the URL which can be used to acquire an authentication token for the current user.
        :return:
        """
        return self.auth.url

    def update_token(self, code, state):
        print("token updated")
        self.client.token = self.auth.request_token(code, state)
        with open(self.token_file, "w") as f:
            f.write(self.client.token.refresh_token)

    def retrieve_token(self):
        if os.path.isfile(self.token_file):
            with open(self.token_file, "r") as f:
                tok = f.read()
                self.client.token = self.creds.refresh_user_token(tok)

    async def update_now_playing(self):
        while 1:
            if self.client.token:
                if self.client.token.is_expiring:
                    self.client.token = self.creds.refresh(self.client.token)
                current_track = await self.client.playback_currently_playing(tracks_only=True)
                pprint(current_track)
            else:
                print(f"No token found. Please authenticate at {self.auth_url()}")
                await asyncio.sleep(5)
