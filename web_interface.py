import asyncio
import re

params_regex = r"code=(\S+)&state=(\S+)\s"


def get_request_handler(spotify):
    """
    Closure which provides an async function to handle authentication requests on behalf of the given Spotify client.
    :return:
    """

    async def handle_authentication_request(reader, writer):
        data = await reader.readuntil()
        message = data.decode()
        if results := re.search(params_regex, message):
            print("Updating Spotify token")
            spotify.update_token(results.group(1), results.group(2))
        writer.write(b"HTTP/1.0 200 OK\r\n\r\nYou may now close this window.\r\n")
        await writer.drain()
        writer.close()

    return handle_authentication_request


async def start_interface(spotify):
    server = await asyncio.start_server(get_request_handler(spotify), "127.0.0.1", 8080)

    async with server:
        print("server running")
        await server.serve_forever()


