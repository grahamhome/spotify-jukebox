# Spotify-Jukebox
Sync your lights and music to make your whole house a jukebox!

## Current progress
* Main service syncs lights with album artwork colors!
  * Lights cycle between complementary colors every 30 sec for duration of song.
  * Checks current song every 3 sec and updates lights when song changes.
  
## Setup
1. Install requirements.txt into a virtual environment and activate it.
1. Complete .env.sample with correct values and rename to .env
- Lifx key can be obtained by visiting https://community.lifx.com/t/creating-a-lifx-http-api-token/25 for instructions.
- Spotify client ID and client secret can be obtained by visiting https://cran.r-project.org/web/packages/spotidy/vignettes/Connecting-with-the-Spotify-API.html and following the instructions.
- Google application credentials can be obtained by visiting https://codelabs.developers.google.com/codelabs/cloud-vision-api-python and following the project setup instructions in Google Cloud.
## Run
`python jukebox.py`