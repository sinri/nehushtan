from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.NehushtanHTTPService import NehushtanHTTPService
from nehushtan.httpd.implement.NehushtanHTTPRouteWithRegexArgs import NehushtanHTTPRouteWithRegexArgs
from nehushtan.httpd.implement.NehushtanHTTPRouteWithRegexKwargs import NehushtanHTTPRouteWithRegexKwargs
from nehushtan.httpd.implement.NehushtanHTTPRouteWithRestFul import NehushtanHTTPRouteWithRestFul
from tests.httpd.TestRequestHandler import TestRequestHandler
from tests.httpd.filter.TestFilter import TestFilter
from tests.httpd.process_chain.TestProcessChainB import TestProcessChainB

TestRequestHandler.router.register_route(
    NehushtanHTTPRouteWithRegexArgs(
        r'^/read/(\d+)$',
        ('tests.httpd.process_chain.TestProcessChainA', 'read'),
        [],
        [NehushtanHTTPConstant.METHOD_GET]
    )
).register_route(
    NehushtanHTTPRouteWithRegexArgs(
        r'/list$',
        (TestProcessChainB, 'list')
    )
).register_route(
    NehushtanHTTPRouteWithRegexArgs(
        r'^/step-in/(\d+)$',
        (TestProcessChainB, 'step3'),
    )
).register_route(
    NehushtanHTTPRouteWithRegexKwargs(
        r'/mix/{index}/name/{name}',
        (TestProcessChainB, 'mix'),
    )
).register_route(
    NehushtanHTTPRouteWithRestFul(
        '/api',
        'tests.httpd.process_chain.api',
        [TestFilter]
    )
)

if __name__ == '__main__':
    NehushtanHTTPService.run_with_threading_server(TestRequestHandler, 4466)
