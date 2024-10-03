import time
from abc import ABC
from typing import Optional

from requests.packages import target

from nehushtan.mysql.MySQLTableExistence import MySQLTableExistence
from nehushtan.mysql.MySQLTableSelection import MySQLTableSelection


class MySQLViewMixin(MySQLTableExistence, ABC):
    """
    For View, actually, READONLY table.
    Since 0.1.4
    """

    @staticmethod
    def now() -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def today() -> str:
        return time.strftime("%Y-%m-%d", time.localtime())

    def select_in_table(self, alias: Optional[str] = None):
        return MySQLTableSelection(
            target=self
            #    model=self, alias=alias
        )
