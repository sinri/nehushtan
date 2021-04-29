from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.NehushtanHTTPRoute import NehushtanHTTPRoute
from nehushtan.httpd.NehushtanHTTPService import NehushtanHTTPService
from tests.httpd.TestRequestHandler import TestRequestHandler

TestRequestHandler.router.register_route(
    NehushtanHTTPRoute(
        r'^/read/(\d+)$',
        [
            ('tests.httpd.process_chain.TestProcessChainA', 'read'),
        ],
        [NehushtanHTTPConstant.METHOD_GET]
    )
)

if __name__ == '__main__':
    NehushtanHTTPService.run_with_threading_server(TestRequestHandler, 4466)
