# Nehushtan Logger Toolkit

## Initialize

Class `NehushtanLogger` is implemented as a wrapper for native `Logger` in Python logging module.

It is recommended to package some functions for loggers with certain handlers, such as following:

```python
def get_logger_for_stdout():
    return NehushtanLogger(
        logger_name="stdout", 
        handlers=(NehushtanLogger.make_stdout_handler(),),
        universal_log_level=logging.INFO
    )

def get_logger_for_stderr():
    return NehushtanLogger(
        logger_name="stderr", 
        handlers=(NehushtanLogger.make_stderr_handler(),),
        universal_log_level=logging.WARNING
    )

def get_logger_for_fixed_file():
    return NehushtanLogger(
        logger_name="runner",
        handlers=(
            NehushtanLogger.make_fixed_file_handler(
                file_name=test_log_store + "/fixed.log"
            ),
        ),
        universal_log_level=logging.INFO
    )

def get_logger_for_rotated_file():
    return NehushtanLogger(
        logger_name="runner",
        handlers=(
            NehushtanLogger.make_timed_rotating_file_handler(
                file_name=test_log_store + "/rotating.log"
            )
        ),
        universal_log_level=logging.INFO
    )
```

## Logging

Several methods for variable level logging provided.

* def debug(self, message: str, extra=None)
* def info(self, message: str, extra=None)
* def warning(self, message: str, extra=None)
* def error(self, message: str, extra=None)
* def exception(self, message: str, exception: BaseException)
* def critical(self, message: str, extra=None)

The `extra` could be anything, and would be tried to print as the string expression of it.

The `exception` method is designed for the try block to print the call stack, and the level of it is `error`. 

## Output Format

```
TIME <LOGGER NAME> [LEVEL] MESSAGE | EXTRA
```

Some samples:

```
2020-11-20 17:59:44,522 <runner> [INFO] 世界还算凑合 | ".../nehushtan/log"
2020-11-20 17:59:44,523 <runner> [WARNING] 世界有点问题 | {"log_path": ".../nehushtan/log"}
2020-11-20 17:59:44,523 <runner> [ERROR] 世界打起来了 | "<nehushtan.logger.NehushtanLogger.NehushtanLogger object at 0x102cf1520>"
2020-11-20 17:59:44,524 <runner> [CRITICAL] 世界马上灭亡 | [3, 2, 1, {"0": [1, 2, 3, {"4": "!"}]}]
2020-11-20 17:59:44,524 <runner> [ERROR] 咕 | "division by zero"
Traceback (most recent call last):
  File ".../nehushtan/tests/test-for-logger.py", line 28, in <module>
    x = 5 / 0
ZeroDivisionError: division by zero
Stack (most recent call last):
  File ".../nehushtan/tests/test-for-logger.py", line 30, in <module>
    shovel_logger.exception("咕", e)
  ...
```

----

Back to [index](./index)