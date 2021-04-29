import json
import re
import socketserver
from abc import abstractmethod
from http.server import BaseHTTPRequestHandler
from typing import Tuple, Iterable
from urllib.parse import parse_qs

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.httpd.NehushtanHTTPConstant import NehushtanHTTPConstant
from nehushtan.httpd.exceptions.NehushtanHTTPError import NehushtanHTTPError
from nehushtan.httpd.exceptions.NehushtanProcessChainIncorrectError import NehushtanProcessChainIncorrectError


class NehushtanHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        # fulfilled by calling method `parse_path`
        self.parsed_path = '/'
        self.parsed_query_dict = {}
        # fulfilled by calling method `parse_body`
        self.raw_body = b''
        self.parsed_body_data = None
        # fulfilled after do_SPAM
        self.method = ''
        #
        self.matched_arguments = []

        self.__process_chain_class = CommonHelper.class_with_class_path(
            'nehushtan.httpd.NehushtanHTTPRequestProcessChain')

        super().__init__(request, client_address, server)

    def prepare_path_and_queries(self):
        # self.path is like path=/ab/c/d?e=f
        parts = self.path.split('?')
        self.parsed_path = parts[0]
        if len(parts) > 1:
            parsed_query_dict = parse_qs(parts[1])
            for k, v in parsed_query_dict.items():
                if k.endswith('[]'):
                    self.parsed_query_dict[k.removesuffix('[]')] = v
                elif len(v) == 1:
                    self.parsed_query_dict[k] = v[0]
                else:
                    self.parsed_query_dict[k] = v

    def prepare_body(self, body_charset=None):
        length = int(self.headers.get('content-length', 0))
        self.raw_body = self.rfile.read(length)
        print(self.raw_body)

        content_type = self.headers.get('content-type', 'text/plain')
        print(content_type)

        if body_charset is None:
            found_charset = re.search(r'charset=(.+);?', content_type, re.I)
            if found_charset:
                body_charset = found_charset.group(1)
            else:
                body_charset = 'utf-8'

        print(body_charset)
        self.raw_body = self.raw_body.decode(body_charset)
        print(self.raw_body)

        if content_type.startswith('application/x-www-form-urlencoded'):
            parsed_body_dict = parse_qs(self.raw_body)
            self.parsed_body_data = {}
            for k, v in parsed_body_dict.items():
                if k.endswith('[]'):
                    self.parsed_body_data[k.removesuffix('[]')] = v
                elif len(v) == 1:
                    self.parsed_body_data[k] = v[0]
                else:
                    self.parsed_body_data[k] = v
        elif content_type.startswith('application/json'):
            self.parsed_body_data = json.loads(self.raw_body)
        else:
            self.parsed_body_data = None

        print(self.parsed_body_data, self.parsed_body_data.get('a', 'c'))

    def do_HEAD(self):
        """
        The HTTP HEAD method requests the headers
            that would be returned if the HEAD request's URL was instead requested with the HTTP GET method.
        For example, if a URL might produce a large download,
            a HEAD request could read its Content-Length header
            to check the filesize without actually downloading the file.

        Request has body	No
        Successful response has body	No
        """
        self.method = NehushtanHTTPConstant.METHOD_HEAD
        self.process_request()

    def do_GET(self):
        """
        Request has body	No
        Successful response has body	Yes
        """
        self.method = NehushtanHTTPConstant.METHOD_GET
        self.process_request()

    def do_POST(self):
        """
        @see https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

        The HTTP POST method sends data to the server.
        The type of the body of the request is indicated by the Content-Type header.

        The difference between PUT and POST is that PUT is idempotent:
            calling it once or several times successively has the same effect (that is no side effect),
            where successive identical POST may have additional effects, like passing an order several times.

        A POST request is typically sent via an HTML form and results in a change on the server.
        In this case, the content type is selected by putting the adequate string
            in the enctype attribute of the <form> element
            or the formenctype attribute of the <input> or <button> elements:

        - application/x-www-form-urlencoded:
            the keys and values are encoded in key-value tuples separated by '&',
            with a '=' between the key and the value.
            Non-alphanumeric characters in both keys and values are percent encoded:
                this is the reason why this type is not suitable to use with binary data
                (use multipart/form-data instead)
        - multipart/form-data:
            each value is sent as a block of data ("body part"),
            with a user agent-defined delimiter ("boundary") separating each part.
            The keys are given in the Content-Disposition header of each part.
        - text/plain

        When the POST request is sent via a method other than an HTML form
            — like via an XMLHttpRequest —
            the body can take any type.
        As described in the HTTP 1.1 specification,
            POST is designed to allow a uniform method to cover the following functions:

        - Annotation of existing resources
        - Posting a message to a bulletin board, newsgroup, mailing list, or similar group of articles;
        - Adding a new user through a signup modal;
        - Providing a block of data, such as the result of submitting a form, to a data-handling process;
        - Extending a database through an append operation.

        Request has body	Yes
        Successful response has body	Yes
        """
        self.method = NehushtanHTTPConstant.METHOD_POST
        self.process_request()

    def do_PUT(self):
        """
        The HTTP PUT request method creates a new resource
            or replaces a representation of the target resource with the request payload.

        The difference between PUT and POST is that PUT is idempotent:
            calling it once or several times successively has the same effect (that is no side effect),
            whereas successive identical POST requests may have additional effects,
            akin to placing an order several times.

        Request has body	Yes
        Successful response has body	No
        """
        self.method = NehushtanHTTPConstant.METHOD_PUT
        self.process_request()

    def do_DELETE(self):
        """
        The HTTP DELETE request method deletes the specified resource.
        Request has body	May
        Successful response has body	May
        """
        self.method = NehushtanHTTPConstant.METHOD_DELETE
        self.process_request()

    def do_OPTIONS(self):
        """
        The HTTP OPTIONS method requests permitted communication options for a given URL or server.
        A client can specify a URL with this method, or an asterisk (*) to refer to the entire server.

        Request has body	No
        Successful response has body	Yes
        """
        self.method = NehushtanHTTPConstant.METHOD_OPTIONS
        self.process_request()

    def do_PATCH(self):
        """
        The HTTP PATCH request method applies partial modifications to a resource.

        PATCH is somewhat analogous to the "update" concept found in CRUD
            (in general, HTTP is different than CRUD, and the two should not be confused).

        A PATCH request is considered a set of instructions on how to modify a resource.
        Contrast this with PUT; which is a complete representation of a resource.

        A PATCH is not necessarily idempotent, although it can be. Contrast this with PUT;
            which is always idempotent.
        The word "idempotent" means that any number of repeated,
            identical requests will leave the resource in the same state.
        For example if an auto-incrementing counter field is an integral part of the resource,
            then a PUT will naturally overwrite it (since it overwrites everything),
            but not necessarily so for PATCH.

        PATCH (like POST) may have side-effects on other resources.

        To find out whether a server supports PATCH,
            a server can advertise its support by adding it to the list
            in the Allow or Access-Control-Allow-Methods (for CORS) response headers.

        Another (implicit) indication that PATCH is allowed,
            is the presence of the Accept-Patch header,
            which specifies the patch document formats accepted by the server.

        Request has body	Yes
        Successful response has body	Yes
        """
        self.method = NehushtanHTTPConstant.METHOD_PATCH
        self.process_request()

    def process_request(self):
        try:
            self.prepare_path_and_queries()

            process_chain_list = self.seek_route_for_process_chains(self.method, self.parsed_path)

            methods_contains_body = (
                NehushtanHTTPConstant.METHOD_POST,
                NehushtanHTTPConstant.METHOD_PUT,
                NehushtanHTTPConstant.METHOD_DELETE,
                NehushtanHTTPConstant.METHOD_PATCH,
            )
            if methods_contains_body.__contains__(self.method):
                self.prepare_body()

            for process_chain in process_chain_list:
                c = CommonHelper.class_with_class_path(process_chain[0])

                # self.log_message(f'{c} against {self.__process_chain_class}')
                if not issubclass(c, self.__process_chain_class):
                    raise NehushtanProcessChainIncorrectError(
                        http_error_message=f'Process Chain Class Error for {process_chain}',
                        http_code=500
                    )

                process_chain_instance = c(self)
                process_chain_instance_target_method = getattr(process_chain_instance, process_chain[1])
                args = self.matched_arguments
                process_chain_instance_target_method(*args)

        except NehushtanHTTPError as http_error:
            self.send_error(http_error.get_http_code(), http_error.http_error_message)
            self.wfile.write(http_error.get_http_error_message().encode())

        # self.send_response(200)
        # self.send_header('content-type', 'text/plain')
        # self.end_headers()
        #
        # self.wfile.write(f'{self.method}\n'.encode())
        #
        # self.wfile.write(f'path: {self.parsed_path}\n'.encode())
        #
        # for k, v in self.parsed_query_dict.items():
        #     self.wfile.write(f'query [{k}] : {v}\n'.encode())
        #
        # self.wfile.write(f'headers: \n{self.headers}'.encode())
        # self.wfile.write(f'Cookie: {self.headers.get("Cookie")}\n'.encode())
        # # self.wfile.write(f'Cookie: {self.headers.get_param("Cookie")}\n'.encode())
        #
        # self.wfile.write(f'Raw Body:\n{self.raw_body}\n'.encode())
        #
        # self.wfile.write(f'Parsed Body:\n{self.parsed_body_data}\n'.encode())

    @abstractmethod
    def seek_route_for_process_chains(self, method: str, path: str) -> Iterable[Tuple[str, str]]:
        """
        You may need to update `self.matched_arguments` here
        """
        pass
