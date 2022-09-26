from quart import Quart
import logging

logger = logging.getLogger("web")

def get_web_server(spotify):
    app = Quart("JukeboxWebServer")

    @app.route("/spotify_auth")
    async def retrive_auth_token(request):
        logger.info(
            f"Got Spotify token for code {request.rel_url.query['code']}, state {request.rel_url.query['state']}")

        await spotify.update_token(request.rel_url.query.get("code"),
                                   request.rel_url.query.get("state"))
        logger.info("Finished updating token")
        return "You may now close this window."

    return app