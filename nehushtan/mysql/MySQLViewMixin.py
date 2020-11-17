import time
from abc import ABC

from mysql.MySQLTableExistence import MySQLTableExistence
from nehushtan.mysql.MySQLTableSelection import MySQLTableSelection


class MySQLViewMixin(MySQLTableExistence, ABC):
    """
    For View, actually, READONLY table.
    Since 0.1.4
    """

    @staticmethod
    def now() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def select_in_table(self):
        return MySQLTableSelection(model=self)