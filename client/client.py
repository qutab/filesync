import asyncio
import logging

from command_generator import get_commands
from dirmonitor import DirMonitor
from request_dispatcher import RequestDispatcher
from shared import argparser


async def do_scan(target_dir, dir_monitor):
    # schedule periodic monitoring of filesystem
    logging.info("scanning files periodically...")
    while True:
        await dir_monitor.scan_fs_contents()
        await asyncio.sleep(2)


async def do_upload(dispatcher, dir_monitor):
    # schedule periodic uploads
    logging.info("syncing files periodically...")
    while True:
        contents = await dir_monitor.get_fs_contents()
        commands = get_commands(*contents)

        await dispatcher.dispatch(commands)
        await asyncio.sleep(2)


async def main():
    # parse args
    parser = argparser.Parser()
    target_dir = parser.target_path
    logging.basicConfig(format='<%(levelname)s>: %(message)s |%(filename)s:%(lineno)d|%(threadName)s',
                        level=logging.DEBUG if parser.verbose else logging.INFO)

    dir_monitor = DirMonitor(target_dir)
    dispatcher = RequestDispatcher(target_dir=target_dir)

    # schedule periodic scans and uploads
    await asyncio.gather(do_scan(target_dir, dir_monitor), do_upload(dispatcher, dir_monitor))


if __name__ == '__main__':
    import sys

    print(sys.version)
    asyncio.run(main())
