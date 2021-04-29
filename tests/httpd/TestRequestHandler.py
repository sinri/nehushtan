import socketserver
from typing import Tuple, Iterable

from nehushtan.httpd.NehushtanHTTPRequestHandler import NehushtanHTTPRequestHandler
from nehushtan.httpd.NehushtanHTTPRouter import NehushtanHTTPRouter


class TestRequestHandler(NehushtanHTTPRequestHandler):
    router = NehushtanHTTPRouter()

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        # self.prepare_router()
        super().__init__(request, client_address, server)

    def seek_route_for_process_chains(self, method: str, path: str) -> Iterable[Tuple[str, str]]:
        route = TestRequestHandler.router.check_request_for_route(method, path)
        # self.log_message(route.path_template)
        self.matched_arguments = route.matched_arguments
        return route.process_chain_list
