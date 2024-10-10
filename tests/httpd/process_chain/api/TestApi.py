from nehushtan.httpd.NehushtanHTTPRequestController import NehushtanHTTPRequestController
from nehushtan.httpd.NehushtanHTTPRequestHandler import NehushtanHTTPRequestHandler


class TestApi(NehushtanHTTPRequestController):
    def __init__(self, http_handler: NehushtanHTTPRequestHandler):
        super().__init__(http_handler)
        print(http_handler.raw_body)

    def hi(self, x):
        self._reply_with_ok({"x": x})
