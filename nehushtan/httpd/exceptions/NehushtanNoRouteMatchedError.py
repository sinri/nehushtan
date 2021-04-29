from nehushtan.httpd.exceptions.NehushtanHTTPError import NehushtanHTTPError


class NehushtanNoRouteMatchedError(NehushtanHTTPError):

    def __init__(self, http_error_message: str, http_code: int):
        self.http_error_message = http_error_message
        self.http_code = http_code
        super().__init__(http_error_message, http_code)
