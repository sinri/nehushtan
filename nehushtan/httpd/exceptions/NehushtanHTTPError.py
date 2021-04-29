class NehushtanHTTPError(Exception):
    def __init__(self, http_error_message: str, http_code: int):
        self.http_error_message = http_error_message
        self.http_code = http_code
        super().__init__(http_error_message)

    def get_http_code(self):
        return self.http_code

    def get_http_error_message(self):
        return self.http_error_message
