from typing import List

from nehushtan.httpd.NehushtanHTTPRoute import NehushtanHTTPRoute
from nehushtan.httpd.exceptions.NehushtanNoRouteMatchedError import NehushtanNoRouteMatchedError


class NehushtanHTTPRouter:
    def __init__(self):
        self.__route_list: List[NehushtanHTTPRoute] = []

    def register_route(self, route: NehushtanHTTPRoute):
        self.__route_list.append(route)
        print(f'NehushtanHTTPRouter::register_route {route}')

    def check_request_for_route(self, method: str, path: str) -> NehushtanHTTPRoute:
        for route in self.__route_list:
            if not route.match_request(method, path):
                continue
            return route

        raise NehushtanNoRouteMatchedError(
            http_error_message=f'Request [{method} {path}] Matched No Rotue.',
            http_code=404
        )
