from nehushtan.httpd.NehushtanHTTPRequestProcessChain import NehushtanHTTPRequestProcessChain


class TestProcessChainB(NehushtanHTTPRequestProcessChain):
    def list(self):
        index = self._get_http_handler().parsed_query_dict.get('index', -1)
        # header_cookie=self._read_header('cookie')
        a = self._read_cookie('a')
        b = self._read_cookie(u'喵')
        self._reply_with_ok(
            {
                "index": index,
                'cookie': self._get_http_handler().parsed_cookie_dict,
                'a': a,
                'b': b
            }
        )

    def step3(self):
        x = self._get_http_handler().get_process_chain_share_data_dict().get('index', 0)
        self._reply_with_ok(x)
