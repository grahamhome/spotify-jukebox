import os
from dotenv import load_dotenv
from pifx import PIFX

load_dotenv()

def main():
    lifx_client = PIFX(os.environ.get("LIFX_KEY"))
    lights = lifx_client.list_lights()
    while True:
        # Get current song from Spotify Player API
        # If new song:
        # Get "Now Playing" album art from Spotify Player API, download it
        ...
        # Get top N colors from album art via GCP Vision API
        ...
        # Set Lifx lights to album colors with Lifx API
        # Set current song


if __name__ == "__main__":
    main()
