import re
from typing import Sequence, Tuple, Union

from nehushtan.httpd.NehushtanHTTPRoute import NehushtanHTTPRoute


class NehushtanHTTPRouteWithRegexArgs(NehushtanHTTPRoute):

    def __init__(
            self,
            path_template: str,
            controller_target: Tuple[Union[type, str], str],
            filter_list: Sequence[Union[type, str]] = None,
            method_options: Sequence[str] = None
    ):
        """
        self.path_template is expected as '^/FIXED/(\\w+)/...$'
        """
        super().__init__()
        self.path_template = path_template
        self.method_options = method_options
        self.filter_list = filter_list if filter_list is not None else []
        self.controller_target = controller_target

    def match_request(self, method: str, path: str) -> bool:
        if self.method_options is not None:
            if not self.method_options.__contains__(method):
                return False

        result = re.search(self.path_template, path)
        if result is None:
            return False

        self.matched_arguments = result.groups()
        # self.matched_keyed_arguments = result.groupdict()
        return True

    def get_filter_list(self) -> Sequence[Union[type, str]]:
        return self.filter_list

    def get_controller_target(self) -> Tuple[Union[type, str], str]:
        return self.controller_target

    def __str__(self):
        method = "|".join(self.method_options) if self.method_options is not None else 'ANY'
        return f'NehushtanHTTPRouteWithRegexArgs [{method}] {self.path_template}'
