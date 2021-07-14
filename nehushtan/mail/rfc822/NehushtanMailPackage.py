import re
from base64 import b64decode
from typing import Optional, Tuple, List

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.mail.rfc2047.EncodedWordsKit import EncodedWordsKit
from nehushtan.mail.rfc822.NehushtanMailContent import NehushtanMailContent


class NehushtanMailPackage:
    """
    Since 0.4.6
    """

    def __init__(self):
        self.meta_dict = {}
        self.raw_body_lines = []
        self.charset = None

        self.content_list: List[NehushtanMailContent] = []

    def __decode_with_charset(self, x: bytes):
        if x is None:
            return None
        if self.charset is None:
            return x.decode('ascii')
        return x.decode(self.charset)

    def get_date(self) -> Optional[str]:
        x = CommonHelper.read_target(self.meta_dict, (b'Date', 0))
        return self.__decode_with_charset(x)

    @staticmethod
    def parse_mail_address_line(x: str):
        print('parse_mail_address_line <-', x)

        # a1@b.c, a2@b.c
        # A1 <a1@b.c>, a2@b.c
        # A1 <a1@b.c>, A2 <a2@b.c>

        email_rule_express = r'([A-Za-z0-9.-]+@[A-Za-z0-9.-]+)|((\S*)\s*<([A-Za-z0-9.-]+@[A-Za-z0-9.-]+)>)'
        address_pieces = re.findall(email_rule_express, x)

        list_of_mail_address_tuple = []
        for address_piece in address_pieces:
            address = None
            name = None
            if address_piece[0]:
                address = address_piece[0]
                name = None
            elif address_piece[2] and address_piece[3]:
                address = address_piece[3]
                name = address_piece[2]
                EncodedWordsKit.decode_string_following_rfc2047(name)

            list_of_mail_address_tuple.append((address, name))
        return list_of_mail_address_tuple

    def get_from_mail_address(self) -> Optional[List[Tuple[str, Optional[str]]]]:
        xs = CommonHelper.read_target(self.meta_dict, (b'From',), [])
        x = b''.join(xs)
        if x:
            x = self.__decode_with_charset(x)
            return NehushtanMailPackage.parse_mail_address_line(x)
        return None

    def get_reply_to_mail_address(self):
        xs = CommonHelper.read_target(self.meta_dict, (b'Reply-To',), [])
        x = b''.join(xs)
        if x:
            x = self.__decode_with_charset(x)
            return NehushtanMailPackage.parse_mail_address_line(x)
        return self.get_from_mail_address()

    def get_to_mail_address(self):
        xs = CommonHelper.read_target(self.meta_dict, (b'To',), [])
        x = b''.join(xs)
        if x:
            x = self.__decode_with_charset(x)
            return NehushtanMailPackage.parse_mail_address_line(x)
        return self.get_from_mail_address()

    def get_subject(self) -> str:
        xs = CommonHelper.read_target(self.meta_dict, (b'Subject',), [])
        s = ''
        for x in xs:
            if type(x) is bytes:
                p = self.__decode_with_charset(x)
                s += EncodedWordsKit.decode_string_following_rfc2047(p)
            if type(x) is not str:
                s += ''
        return s

    def get_content_type(self) -> Optional[str]:
        x_array = CommonHelper.read_target(self.meta_dict, (b'Content-Type',), [])
        s = ''
        for x in x_array:
            if type(x) is bytes:
                x = x.decode('ascii')
            s += x
        return s

    def get_content_transfer_encoding(self):
        x = CommonHelper.read_target(self.meta_dict, (b'Content-Transfer-Encoding', 0))
        if type(x) is bytes:
            x = x.decode('ascii')
        return x

    def get_parsed_body_text(self):
        x = b''
        for line in self.raw_body_lines[1:-2]:
            # print("> ", line)

            if line == b'This is a multi-part message in MIME format.':
                return self.__handle_mime_multi_part_body(self.raw_body_lines[3:-2])

            x += line
        if self.get_content_transfer_encoding() == 'base64':
            x = b64decode(x)
            if self.charset is None:
                x = x.decode()
            else:
                x = x.decode(self.charset)

        return x

    def __handle_mime_multi_part_body(self, lines: List[bytes]):
        """
        See https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html

        TODO 解析每个piece内的header
        """
        boundary = lines[0]

        pieces = []
        buffer = []
        for line in lines[2:]:
            if line == boundary or line[:-2] == boundary:
                piece = b"".join(buffer)
                if self.get_content_transfer_encoding() == 'base64':
                    piece = b64decode(piece)
                if self.charset is None:
                    piece = piece.decode()
                else:
                    piece = piece.decode(self.charset)

                pieces.append(piece)

                buffer = []
            else:
                if line == b'':
                    continue
                buffer.append(line)
        # print('@',buffer)
        # piece = b"".join(buffer)
        # if self.get_content_transfer_encoding() == 'base64':
        #     piece = b64decode(piece)
        # if self.charset is None:
        #     piece = piece.decode()
        # else:
        #     piece = piece.decode(self.charset)
        # pieces.append(piece)

        # print(pieces)
        return "\n".join(pieces)

    def update_for_charset(self):
        self.charset = None
        content_type = self.get_content_type()
        # print('update_for_charset by ',content_type)
        if content_type:
            matched = re.match(r'.*charset=\"(.+)\"', content_type)
            # print('matched',matched)
            if matched:
                self.charset = matched[1]

    def show_debug_info(self):
        print("CHARSET is ", self.charset)
        print('Meta:')
        print('DATE', self.get_date())
        print('FROM', self.get_from_mail_address())
        print('REPLY TO', self.get_reply_to_mail_address())
        print('TO', self.get_to_mail_address())
        print('SUBJECT', self.get_subject())
        print('CONTENT-TYPE', self.get_content_type())
        print('CONTENT-TRANSFER-ENCODING', self.get_content_transfer_encoding())
        # for k, v in self.meta_dict.items():
        #     print(f'`{k}` -> `{v}`')
        print('Body:')
        # for line in self.raw_body_lines:
        #     print(line)
        print(self.get_parsed_body_text())
        print(' - - - - - ')
