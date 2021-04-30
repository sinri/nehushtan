import json
import re

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.NehushtanHTTPRequestHandler import NehushtanHTTPRequestHandler
from nehushtan.httpd.exceptions.NehushtanRequestParameterError import NehushtanRequestParameterError


class NehushtanHTTPRequestProcessChain:
    def __init__(self, http_handler: NehushtanHTTPRequestHandler):
        self.__http_handler = http_handler

    def _get_http_handler(self) -> NehushtanHTTPRequestHandler:
        return self.__http_handler

    def __clean_paramter_with_regex(self, read_value, value_regex: str, key: str, key_type: str):
        if read_value is None:
            raise NehushtanRequestParameterError(
                key,
                key_type,
                NehushtanRequestParameterError.DESC_NOT_SET
            )
        if value_regex is not None:
            x = f'{read_value}'
            found = re.search(value_regex, x)
            if found is None:
                raise NehushtanRequestParameterError(
                    key,
                    key_type,
                    NehushtanRequestParameterError.DESC_FORMAT_ERROR
                )
        return read_value

    def _read_query(self, key: tuple, default=None):
        return CommonHelper.read_target(self._get_http_handler().parsed_query_dict, key, default)

    def _read_query_indispensably(self, key: tuple, value_regex: str = None):
        x = self._read_query(key)
        return self.__clean_paramter_with_regex(x, value_regex, f'{key}', NehushtanRequestParameterError.TYPE_QUERY)

    def _read_body(self, key: tuple, default=None):
        return CommonHelper.read_target(self._get_http_handler().parsed_body_data, key, default)

    def _read_body_indispensably(self, key: tuple, value_regex: str = None):
        x = self._read_body(key)
        return self.__clean_paramter_with_regex(x, value_regex, f'{key}', NehushtanRequestParameterError.TYPE_BODY)

    def _read_header(self, key: str, default: str = None):
        return self._get_http_handler().headers.get(key, default)

    def _read_cookie(self, key: str, default: str = None):
        return CommonHelper.read_target(self._get_http_handler().parsed_cookie_dict, (key,), default)

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
