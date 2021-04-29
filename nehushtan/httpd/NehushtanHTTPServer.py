from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Tuple, Callable


class NehushtanHTTPServer(ThreadingHTTPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: Callable[..., BaseHTTPRequestHandler]):
        super().__init__(server_address, RequestHandlerClass)
