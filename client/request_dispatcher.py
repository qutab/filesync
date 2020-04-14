import asyncio
import pathlib
from urllib.parse import urljoin

from aiohttp import ClientSession


class RequestDispatcher:
    def __init__(self, **kwargs):
        self._request = Request(**kwargs)
        self._target_dir = kwargs['target_dir']

    async def dispatch(self, commands: dict):
        requests = [
            asyncio.create_task(
                self._request.post_to_server(file, cmd[0], cmd[1:])
            ) for file, cmd in commands.items()
        ]
        await asyncio.gather(*requests)
        return True


class Request:
    def __init__(self, host="localhost", port=9999, target_dir=pathlib.Path.cwd()):
        self._url = "http://{host}:{port}".format(host=host, port=port)
        self._response = None
        self._target_dir = target_dir

    async def post_to_server(self, filename, action, args):
        fullname = self._target_dir.joinpath(filename)
        if fullname.is_file():
            data = {
                'file': open(str(fullname), 'rb'),
                'relative_path': filename
            }
        else:
            data = {
                'relative_path': filename
            }

        async with ClientSession() as session:
            async with session.post(urljoin(self._url, str(action).lower()), data=data) as resp:
                await resp.text()
                return resp.status
