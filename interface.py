from fastapi import FastAPI, Request
import logging

logger = logging.getLogger("web")


def jukebox_web_interface_factory(spotify_client):
    app = FastAPI()

    @app.get("/")
    async def handle_auth_request(request: Request):
        logger.info("Handling request made to authentication endpoint")
        data = await request.json()
        if (code := data.get("code")) and (state := data.get("state")):
            await spotify_client.update_token(code, state)

    return app

