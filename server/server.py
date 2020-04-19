import logging
import signal
import sys

import sync_server as ss

from shared import argparser


def signal_handler(server):
    print('SIGINT received')
    server.stop()
    sys.exit(0)


def main():
    # parse args
    parser = argparser.Parser()
    logging.basicConfig(format='<%(levelname)s>: %(message)s |%(filename)s:%(lineno)d|%(threadName)s',
                        level=logging.DEBUG if parser.verbose else logging.INFO)

    server = ss.HttpServer()
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(server))
    server.start()


if __name__ == '__main__':
    main()
