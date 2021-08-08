import os

import spotipy
from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)

cache_path = './.spotify_cache'


@app.route('/')
def index():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=cache_path)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-read-currently-playing playlist-modify-private',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Handle callback from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return "You may now close this page."


"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""


def main():
    load_dotenv()
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))


if __name__ == '__main__':
    main()

