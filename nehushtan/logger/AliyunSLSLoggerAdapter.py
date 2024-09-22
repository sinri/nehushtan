import json
import time

from aliyun.log import LogClient, PutLogsRequest, LogItem, LogException

from nehushtan.helper.CommonHelper import CommonHelper
from nehushtan.logger.NehushtanLogger import NehushtanLoggerAdapter, NehushtanLogLevel


class AliyunSLSLoggerAdapter(NehushtanLoggerAdapter):
    """
    Adapter for Aliyun SLS.
    Requirement `aliyun-log-python-sdk` (such as 0.9.11) should be declared.
    Since 0.5.1.
    """

    def __init__(self,
                 endpoint: str,
                 access_key_id: str,
                 access_key_secret: str,
                 project: str,
                 logstore: str,
                 source: str,
                 ):
        super().__init__()
        self.__client = LogClient(endpoint, access_key_id, access_key_secret)
        self.__logstore = logstore
        self.__project = project
        self.__source = source.replace('[IP]', CommonHelper.get_local_ip())

    def write_one_log(self, level: NehushtanLogLevel, contents: dict):
        # topic = contents['topic']
        # del contents['topic']
        contents['level'] = level.name

        l = []
        for (k, v) in contents.items():
            if v is None:
                l.append((k, None,))
            elif isinstance(v, str):
                l.append((k, v))
            else:
                l.append((k, json.dumps(v, default=lambda x: x.__str__(), ensure_ascii=False)))

        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents(l)

        req2 = PutLogsRequest(
            project=self.__project,
            logstore=self.__logstore,
            topic=self.get_topic(),
            source=self.__source,
            logitems=[log_item]
        )
        try:
            self.__client.put_logs(req2)
        except LogException as e:
            print(e)
