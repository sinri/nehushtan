from typing import List


class NehushtanMailContent:
    def __init__(self):
        self.content_type = b''
        self.raw_content: List[bytes] = []
        self.boundary = None
        self.sub_content_list: List['NehushtanMailContent'] = []

    def set_content_type(self, content_type: bytes):
        self.content_type = content_type
        return self

    def set_boundary(self, boundary: bytes):
        self.boundary = boundary
        return self

    def append_raw_content_row(self, row: bytes):
        self.raw_content.append(row)
        return self

    def append_sub_content(self, sub_content: 'NehushtanMailContent'):
        self.sub_content_list.append(sub_content)
        return self
