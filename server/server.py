import logging
import threading

from server import sync_server as ss
from shared import argparser


def main():
    # parse args
    parser = argparser.Parser()
    logging.basicConfig(format='<%(levelname)s>: %(message)s |%(filename)s:%(lineno)d|%(threadName)s',
                        level=logging.DEBUG if parser.verbose else logging.INFO)

    server = ss.HttpServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("SIGINT received")
        threading.Thread(target=lambda: server.stop(), daemon=True).start()


if __name__ == '__main__':
    main()
