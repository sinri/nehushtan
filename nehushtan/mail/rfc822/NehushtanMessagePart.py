from email.message import EmailMessage, Message
from typing import Union, Optional, List


class NehushtanMessagePart:
    def __init__(self, msg: Union[EmailMessage, Message], parent: Optional['NehushtanMessagePart']):
        self.__parent = parent
        self.__message = msg
        self.__sub_message_list: List['NehushtanMessagePart'] = []

        self.__organize_parts()

    def get_parent(self):
        return self.__parent

    def get_message(self):
        return self.__message

    def get_sub_message_list(self):
        return self.__sub_message_list

    # def append_sub_message(self, sub_message):
    #     self.__sub_message_list.append(sub_message)
    #     return self

    def __organize_parts(self):
        if self.__message.is_multipart():
            for part in self.__message.iter_parts():
                self.__sub_message_list.append(NehushtanMessagePart(part, self))
