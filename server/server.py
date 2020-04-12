import syncserver as ss

import signal
import sys


def signal_handler(server):
    print('SIGINT received')
    server.stop()
    sys.exit(0)


def main():
    server = ss.HttpServer()
    signal.signal(signal.SIGINT, lambda signum, frame: signal_handler(server))
    server.start()


if __name__ == '__main__':
    main()
