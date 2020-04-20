import asyncio
import logging
import zlib
from pathlib import Path
from urllib.parse import urljoin

from aiohttp import ClientSession, client_exceptions

from shared import argparser


class RequestDispatcher:
    """
    Creates requests from commands which will be sent to the server
    """

    def __init__(self, **kwargs):
        self._request = Request(**kwargs)

    async def dispatch(self, commands: dict):
        """
        Dispatch requests to server asynchronously for each command
        """
        logging.debug(f"Commands to be dispatched {commands}")

        requests = [
            asyncio.create_task(
                self._request.post_to_server(file, cmd[0], cmd[1:])
            ) for file, cmd in commands.items()
        ]
        await asyncio.gather(*requests)
        return True


class Request:
    """
    Helper class to post requests to server
    """

    def __init__(self, host: str = "localhost", port: int = 9999, target_dir: Path = Path.cwd()):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = None
        self._target_dir = target_dir
        self._compressed = argparser.Parser().compressed

    async def post_to_server(self, relative_path: str, action: str, args: str):
        """
        Send a single post requests to server
        """
        fullname = self._target_dir.joinpath(relative_path)
        data = {'relative_path': relative_path}

        if fullname.exists() and fullname.is_file():
            if self._compressed:
                data['file'] = zlib.compress(open(str(fullname), 'rb').read())
            else:
                data['file'] = open(str(fullname), 'rb')

        try:
            async with ClientSession() as session:
                url = urljoin(self._url, str(action).lower())
                logging.debug(f"Posting to url: {url}")

                async with session.post(url, data=data) as resp:
                    await resp.text()
                    return resp.status
        except client_exceptions.ClientConnectorError as exc:
            logging.error(exc)
        except client_exceptions.ServerDisconnectedError:
            logging.error("Server must be started first")
            for task in asyncio.Task.all_tasks():
                task.cancel()
