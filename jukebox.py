import logging.config
import json
from aiohttp import web

with open("logging/logging_config.json", "r") as f:
    logging.config.dictConfig(config=json.load(f))
import asyncio

from dotenv import load_dotenv

from lifx.lifx import Lifx
from song import Song
from spotify.spotify import Spotify
from web.web_interface import start_web_interface


logger = logging.getLogger("jukebox")

def main():
    logger.info("Jukebox started")
    load_dotenv()
    loop = asyncio.new_event_loop()
    now_playing = Song()
    spotify = Spotify(now_playing)
    lifx = Lifx(now_playing, loop)

    async def run():
        await asyncio.gather(web._run_app(start_web_interface(spotify), host="127.0.0.1"), spotify.retrieve_token(), spotify.update_now_playing(), spotify.update_pause_state(), lifx.setup(), lifx.follow())

    loop.create_task(run())

    loop.run_forever()


if __name__ == "__main__":
    main()
