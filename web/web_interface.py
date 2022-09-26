from aiohttp import web
import json
import logging

logger = logging.getLogger("web")


async def start_web_interface(spotify):
    async def provide_song_data(self):
        logger.info("Got song data request")
        logger.info(f"Returning: {json.dumps(spotify.now_playing.__dict__, indent=4)}")
        return web.json_response(status=200, data=spotify.now_playing.__dict__)

    async def retrive_auth_token(self, request):
        logger.info(
            f"Got Spotify token for code {request.rel_url.query['code']}, state {request.rel_url.query['state']}"
        )

        await spotify.update_token(request.rel_url.query.get("code"), request.rel_url.query.get("state"))
        logger.info("Finished updating token")
        return web.Response(status=200, text="You may now close this window.")

    app = web.Application()

    app.router.add_get("/spotify_auth{tail:.*}", retrive_auth_token)
    app.router.add_get("/song_data", provide_song_data)
    logger.info("Web interface will start")

    return app
