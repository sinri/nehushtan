from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.NehushtanHTTPRoute import NehushtanHTTPRoute
from nehushtan.httpd.NehushtanHTTPService import NehushtanHTTPService
from tests.httpd.TestRequestHandler import TestRequestHandler
from tests.httpd.process_chain.TestProcessChainA import TestProcessChainA
from tests.httpd.process_chain.TestProcessChainB import TestProcessChainB

TestRequestHandler.router.register_route(
    NehushtanHTTPRoute(
        r'^/read/(\d+)$',
        [
            ('tests.httpd.process_chain.TestProcessChainA', 'read'),
        ],
        [NehushtanHTTPConstant.METHOD_GET]
    )
).register_route(
    NehushtanHTTPRoute(
        r'/list$',
        [
            (TestProcessChainB, 'list')
        ]
    )
).register_route(
    NehushtanHTTPRoute(
        r'^/step-in/(\d+)$',
        [
            (TestProcessChainA, 'step1'),
            (TestProcessChainA, 'step2'),
            (TestProcessChainB, 'step3'),
        ]
    )
)

if __name__ == '__main__':
    NehushtanHTTPService.run_with_threading_server(TestRequestHandler, 4466)
