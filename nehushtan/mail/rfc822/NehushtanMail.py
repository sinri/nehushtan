import json
from typing import List

from nehushtan.mail.rfc822.NehushtanMailPackage import NehushtanMailPackage


class NehushtanMail:
    """
    This class works following RFC822
    """

    def __init__(self):
        self.packages: List[NehushtanMailPackage] = []

    def set_packages(self, packages: List[NehushtanMailPackage]):
        self.packages = packages
        return self

    def get_last_package(self):
        return self.packages[-1]

    @staticmethod
    def make_mail_by_rfc822_content(raw_mail_text: str):
        print(raw_mail_text)

        lines = raw_mail_text.split("\r\n")

        packages = []
        current_package = None

        buffer_key = None
        buffer_content = []

        for line in lines:
            print('> ' + json.dumps(line))
            if line.startswith("Received:"):
                if current_package is not None:
                    packages.append(current_package)
                current_package = NehushtanMailPackage()
                buffer_key = None
                buffer_content = []

            if line.startswith("\t"):
                buffer_content.append(line.lstrip("\t"))
            elif line.startswith("        "):
                buffer_content.append(line.lstrip("        "))
            elif line.startswith("    "):
                buffer_content.append(line.lstrip("    "))
            else:
                key_end_index = line.find(":")
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
        if current_package is not None:
            packages.append(current_package)

        print(' = = = = = ')
        for package in packages:
            package.show_debug_info()

        received_mail = NehushtanMail().set_packages(packages)
        return received_mail
