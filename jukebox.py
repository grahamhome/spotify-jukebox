import asyncio

from dotenv import load_dotenv
from song import NowPlaying
from spotify import Spotify
from web_interface import start_interface

now_playing = NowPlaying.get()
spotify = Spotify(now_playing)

if __name__ == "__main__":
    load_dotenv()
    loop = asyncio.new_event_loop()
    loop.create_task(spotify.update_now_playing())
    loop.run_until_complete(start_interface(spotify))
    loop.run_forever()

