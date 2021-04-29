from nehushtan.httpd.NehushtanHTTPRequestProcessChain import NehushtanHTTPRequestProcessChain


class TestProcessChainA(NehushtanHTTPRequestProcessChain):
    def read(self, index: int):
        # self.get_http_handler().log_message('emmm')
        # self._get_http_handler().send_response(200)
        # self._get_http_handler().send_header('content-type', 'text/plain')
        # self._get_http_handler().end_headers()
        # self._get_http_handler().wfile.write(f'READ INDEX [{index}]'.encode())
        self._reply_with_ok({'index': index})
