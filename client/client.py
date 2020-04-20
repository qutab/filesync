import asyncio
import logging

from client.command_generator import get_commands
from client.dir_monitor import DirMonitor
from client.request_dispatcher import RequestDispatcher
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


async def main(target_dir, dir_monitor, dispatcher):
    # schedule periodic scans and uploads
    await asyncio.gather(do_scan(target_dir, dir_monitor), do_upload(dispatcher, dir_monitor))


def do_setup():
    # parse args
    parser = argparser.Parser()
    target_dir = parser.target_path
    logging.basicConfig(format='<%(levelname)s>: %(message)s |%(filename)s:%(lineno)d|%(threadName)s',
                        level=logging.DEBUG if parser.verbose else logging.INFO)

    dir_monitor = DirMonitor(target_dir)
    dispatcher = RequestDispatcher(target_dir=target_dir)

    return target_dir, dir_monitor, dispatcher


if __name__ == '__main__':
    import sys

    print(sys.version)
    assert sys.version_info.major == 3 and sys.version_info.minor >= 7

    try:
        asyncio.run(main(*do_setup()))
    except (asyncio.CancelledError, KeyboardInterrupt):
        logging.info(f"Client tasks cancelled")
