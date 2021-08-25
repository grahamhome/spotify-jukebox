from fastapi import FastAPI, Request


def jukebox_web_interface_factory(spotify_client):
    app = FastAPI()

    @app.get("/")
    async def handle_auth_request(request: Request):
        data = await request.json()
        if (code := data.get("code")) and (state := data.get("state")):
            await spotify_client.update_token(code, state)

    return app

