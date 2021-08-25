import asyncio

from dotenv import load_dotenv

from lifx import Lifx
from song import Song
from spotify import Spotify
from web_interface import start_interface


def main():
    load_dotenv()
    loop = asyncio.new_event_loop()
    now_playing = Song()
    spotify = Spotify(now_playing)
    lifx = Lifx(now_playing, loop)

    async def run():
        await asyncio.gather(spotify.retrieve_token(), spotify.update_now_playing(), spotify.update_pause_state(), lifx.setup(), lifx.follow())

    loop.create_task(run())
    loop.run_until_complete(start_interface(spotify))

    loop.run_forever()


if __name__ == "__main__":
    main()