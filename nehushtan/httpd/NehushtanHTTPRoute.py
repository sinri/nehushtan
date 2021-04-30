import re
from typing import Tuple, List, Sequence, Union


class NehushtanHTTPRoute:

    def __init__(
            self,
            path_template: str,
            process_chain_list: Sequence[Tuple[Union[type, str], str]],
            method_options: List[str] = None
    ):
        self.path_template = path_template
        self.process_chain_list = process_chain_list
        self.method_options = method_options

        self.matched_arguments = []

    def match_request(self, method: str, path: str) -> bool:
        if self.method_options is not None:
            if not self.method_options.__contains__(method):
                return False

        result = re.search(self.path_template, path)
        if result is None:
            return False

        self.matched_arguments = result.groups()
        return True

    def get_matched_arguments(self) -> List[str]:
        return self.matched_arguments
