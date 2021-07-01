import re
from base64 import b64decode
from typing import Optional, Tuple

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.mail.rfc2047.EncodedWordsKit import EncodedWordsKit


class NehushtanMailPackage:
    def __init__(self):
        self.meta_dict = {}
        self.raw_body_lines = []

    def get_date(self) -> Optional[str]:
        return CommonHelper.read_target(self.meta_dict, ('Date', 0))

    @staticmethod
    def parse_mail_address_line(x: str):
        name, address = x.split(" ")
        name = EncodedWordsKit.decode_string_following_rfc2047(name)
        address: str = address[1:-1]
        return address, name

    def get_from_mail_address(self) -> Optional[Tuple[str, str]]:
        x = CommonHelper.read_target(self.meta_dict, ('From', 0))
        if x:
            return NehushtanMailPackage.parse_mail_address_line(x)
        return None

    def get_reply_to_mail_address(self):
        x = CommonHelper.read_target(self.meta_dict, ('Reply-To', 0))
        if x:
            return NehushtanMailPackage.parse_mail_address_line(x)
        return self.get_from_mail_address()

    def get_to_mail_address(self):
        x = CommonHelper.read_target(self.meta_dict, ('To', 0))
        if x:
            return NehushtanMailPackage.parse_mail_address_line(x)
        return self.get_from_mail_address()

    def get_subject(self) -> str:
        x = CommonHelper.read_target(self.meta_dict, ('Subject', 0))
        if type(x) is str:
            return EncodedWordsKit.decode_string_following_rfc2047(x)
        else:
            return ''

    def get_content_type(self) -> Optional[str]:
        x = CommonHelper.read_target(self.meta_dict, ('Content-Type', 0))
        return x

    def get_content_transfer_encoding(self):
        x = CommonHelper.read_target(self.meta_dict, ('Content-Transfer-Encoding', 0))
        return x

    def get_parsed_body_text(self):
        x = ''
        for line in self.raw_body_lines[1:-2]:
            x += line
        if self.get_content_transfer_encoding() == 'base64':
            x = b64decode(x)

            encoding = None
            content_type = self.get_content_type()
            if content_type:
                matched = re.match(r'charset="(.+)"', content_type)
                if matched:
                    encoding = matched[1]
            if encoding is None:
                x = x.decode()
            else:
                x = x.decode(encoding)

        return x

    def show_debug_info(self):
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
