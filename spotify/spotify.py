import aiofiles
import tekore as tk
import asyncio
import os
import logging

from song import Song


class Spotify:
    """
    Interface to the Spotify API
    """

    token_file = "spotify/spotify_token.tok"
    logger = logging.getLogger("spotify")

    def __init__(self, now_playing: Song):
        self.config = tk.config_from_environment()
        self.creds = tk.Credentials(*self.config)
        self.auth = tk.UserAuth(self.creds, tk.scope.user_read_currently_playing)
        self.client = tk.Spotify(asynchronous=True)
        self.now_playing = now_playing
        self.logger.info("Spotify client created")

    def auth_url(self):
        """
        Returns the URL which can be used to acquire an authentication token for the current user.
        :return:
        """
        return self.auth.url

    async def update_token(self, code, state):
        self.client.token = self.auth.request_token(code, state)
        file = await aiofiles.open(self.token_file, mode="w")
        await file.write(self.client.token.refresh_token)
        await file.close()

    async def retrieve_token(self):
        if os.path.isfile(self.token_file):
            file = await aiofiles.open(self.token_file, mode="r")
            tok = await file.read()
            await file.close()
            self.client.token = self.creds.refresh_user_token(tok)
        else:
            print(f"No token found. Please authenticate at {self.auth_url()}")

    async def update_pause_state(self):
        while 1:
            if self.client.token:
                if self.client.token.is_expiring:
                    self.client.token = self.creds.refresh(self.client.token)
                current_track_data = await self.client.playback_currently_playing()
                if current_track_data:
                    self.now_playing.paused = not current_track_data.is_playing
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    async def update_now_playing(self):
        while 1:
            if self.client.token:
                if self.client.token.is_expiring:
                    self.client.token = self.creds.refresh(self.client.token)
                current_track_data = await self.client.playback_currently_playing()
                if (
                    current_track_data
                    and current_track_data.item
                    and current_track_data.item.id != self.now_playing.spotify_id
                ):
                    self.logger.info(f"New song detected: {current_track_data.item.name}")
                    await self.now_playing.update(
                        spotify_id=current_track_data.item.id,
                        title=current_track_data.item.name,
                        artists=[artist.name for artist in current_track_data.item.artists],
                        album=current_track_data.item.album.name,
                        album_art=max(
                            current_track_data.item.album.images,
                            key=lambda image: image.height,
                        ).url,
                        lyrics="",
                    )
                await asyncio.sleep(3)
            else:
                await asyncio.sleep(1)
