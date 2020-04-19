import asyncio
import logging
from pathlib import Path
from urllib.parse import urljoin

from aiohttp import ClientSession, client_exceptions


class RequestDispatcher:
    def __init__(self, **kwargs):
        self._request = Request(**kwargs)

    async def dispatch(self, commands: dict):
        logging.debug(f"Commands to be dispatched {commands}")

        requests = [
            asyncio.create_task(
                self._request.post_to_server(file, cmd[0], cmd[1:])
            ) for file, cmd in commands.items()
        ]
        await asyncio.gather(*requests)
        return True


class Request:
    def __init__(self, host: str="localhost", port: int=9999, target_dir: Path=Path.cwd()):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = None
        self._target_dir = target_dir

    async def post_to_server(self, relative_path: str, action: str, args: str):
        fullname = self._target_dir.joinpath(relative_path)
        data = {'relative_path': relative_path}
        if fullname.exists() and fullname.is_file():
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
