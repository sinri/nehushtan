import logging

from nehushtan.logger.NehushtanLogger import NehushtanLogger
from tests.config import test_log_store

shovel_logger = NehushtanLogger(
    logger_name="runner",
    handlers=(
        NehushtanLogger.make_stdout_handler(),
        NehushtanLogger.make_stderr_handler(),
        NehushtanLogger.make_fixed_file_handler(
            file_name=test_log_store + "/fixed.log"
        ),
        NehushtanLogger.make_timed_rotating_file_handler(
            file_name=test_log_store + "/rotating.log"
        )
    ),
    universal_log_level=logging.INFO
)

shovel_logger.debug('世界非常和平')
shovel_logger.info('世界还算凑合', test_log_store)
shovel_logger.warning('世界有点问题', {"log_path": test_log_store})
shovel_logger.error('世界打起来了', shovel_logger)
shovel_logger.critical('世界马上灭亡', [3, 2, 1, {0: [1, 2, 3, {4: "!"}]}])

try:
    x = 5 / 0
except Exception as e:
    shovel_logger.exception("咕", e)
