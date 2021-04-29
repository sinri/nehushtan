import json

from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.NehushtanHTTPRequestHandler import NehushtanHTTPRequestHandler


class NehushtanHTTPRequestProcessChain:
    def __init__(self, http_handler: NehushtanHTTPRequestHandler):
        self.__http_handler = http_handler

    def _get_http_handler(self) -> NehushtanHTTPRequestHandler:
        return self.__http_handler

    def _reply(self, text: str, http_code: int = 200, header_dict: dict = None, encoding: str = None):
        if encoding is not None:
            s = text.encode(encoding)
        else:
            s = text.encode()

        self._get_http_handler().send_response(http_code)

        if header_dict is None:
            header_dict = {}
        header_dict['Content-Length'] = '%i' % len(s)
        for k, v in header_dict.items():
            self._get_http_handler().send_header(k, v)
        self._get_http_handler().end_headers()

        self._get_http_handler().wfile.write(s)

    def _reply_with_text(self, text: str, http_code: int = 200, encoding: str = None):
        self._reply(
            text,
            http_code,
            {NehushtanHTTPConstant.HEADER_CONTENT_TYPE: NehushtanHTTPConstant.HEADER_CONTENT_TYPE_VALUE_TEXT},
            encoding
        )

    def _reply_with_json(self, anything, http_code: int = 200, encoding: str = None):
        s = json.dumps(anything)

        self._reply(
            s,
            http_code,
            {NehushtanHTTPConstant.HEADER_CONTENT_TYPE: NehushtanHTTPConstant.HEADER_CONTENT_TYPE_VALUE_JSON},
            encoding
        )

    def _reply_with_ok(self, anything, encoding: str = None):
        self._reply_with_json({"code": NehushtanHTTPConstant.REPLY_CODE_OK, "data": anything}, 200, encoding)

    def _reply_with_fail(self, anything, encoding: str = None):
        self._reply_with_json({"code": NehushtanHTTPConstant.REPLY_CODE_FAIL, "data": anything}, 200, encoding)
