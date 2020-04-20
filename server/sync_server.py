import logging
import socketserver
from abc import ABC, abstractmethod

from server import request_handler as rh


class SyncServer(ABC):
    """Abstract base class for server's sync operations"""

    @abstractmethod
    def start(self):
        raise NotImplementedError('Derived class must implement this method')

    @abstractmethod
    def stop(self):
        raise NotImplementedError('Derived class must implement this method')


class HttpServer(SyncServer):
    server_version = 'HttpServer/1.1'

    def __init__(self, host="localhost", port=9999):
        self._host = host
        self._port = port
        self._server = socketserver.TCPServer((self._host, self._port), rh.RequestHandler)

    def start(self):
        logging.info("Starting HTTP server...")
        self._server.serve_forever()

    def stop(self):
        logging.info("Stopping HTTP server...")
        self._server.shutdown()
