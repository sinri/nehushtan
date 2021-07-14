import re
from typing import List

from nehushtan.logger.NehushtanFileLogger import NehushtanFileLogger
from nehushtan.logger.NehushtanLogging import NehushtanLogging
from nehushtan.mail.rfc822.NehushtanMailContent import NehushtanMailContent
from nehushtan.mail.rfc822.NehushtanMailPackage import NehushtanMailPackage


class NehushtanMail:
    """
    This class works following RFC822
    Since 0.4.6
    """

    def __init__(self):
        self.packages: List[NehushtanMailPackage] = []

    def set_packages(self, packages: List[NehushtanMailPackage]):
        self.packages = []
        for package in packages:
            self.append_package(package)
        return self

    def append_package(self, package: NehushtanMailPackage):
        package.update_for_charset()
        self.packages.append(package)
        return self

    def get_last_package(self):
        return self.packages[-1]

    @staticmethod
    def make_mail_by_rfc822_content(raw_mail_bytes: bytes, logger: NehushtanFileLogger = None):
        logger.debug('make_mail_by_rfc822_content raw_mail_bytes: \n')
        logger.write_raw_line_to_log(raw_mail_bytes.decode('ascii'), NehushtanLogging.DEBUG)
        logger.debug('\n')

        lines = raw_mail_bytes.split(b"\r\n")

        packages = []
        current_package = None

        buffer_key = None
        buffer_content = []

        body_started = False
        body_rows = []

        for line in lines:
            # print('> ', line)
            if line.startswith(b"Received:"):
                if current_package is not None:
                    packages.append(current_package)
                current_package = NehushtanMailPackage()
                buffer_key = None
                buffer_content = []

            if line.startswith(b"Content-Type:"):
                body_started = True
            if body_started:
                body_rows.append(line)
                continue

            if current_package is None:
                current_package = NehushtanMailPackage()

            prefix_as_whites = re.match(b'^\s+', line)
            if prefix_as_whites:
                buffer_content.append(line[len(prefix_as_whites.group(0)):])
                logger.info('appended to buffer: ' + line[len(prefix_as_whites.group(0)):].decode())
            else:
                key_end_index = line.find(b":")
                if key_end_index < 0:
                    current_package.raw_body_lines.append(line)
                else:
                    # new buffer start!
                    if buffer_key is not None:
                        current_package.meta_dict[buffer_key] = buffer_content
                        buffer_content = []

                    buffer_key = line[:key_end_index]
                    buffer_content.append(line[key_end_index + 2:])

        if buffer_key is not None:
            current_package.meta_dict[buffer_key] = buffer_content

        contents = NehushtanMail.__parse_body_rows(body_rows, logger)

        if current_package is not None:
            for content in contents:
                current_package.content_list.append(content)

            # print(len(packages))
            packages.append(current_package)
            # print("~~~")
            # print(len(packages))

        received_mail = NehushtanMail().set_packages(packages)

        # print(' = = = = = ')
        # for package in received_mail.packages:
        #     package.show_debug_info()

        return received_mail

    @staticmethod
    def __parse_body_rows(body_rows: List[bytes], logger: NehushtanFileLogger = None) -> List[NehushtanMailContent]:
        pass
