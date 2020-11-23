# Nehushtan 

A set of Python Toolkits

## CLI 

Class `NehushtanArgumentParser` can parse command line arguments to dict.

`python3 any.py -s a --long b --prefix-c d`

would be finally parsed into 

```
{"s":"a","long":"b","prefix":{"c":"d"}}
```

## Common Helper

Class `CommonHelper` makes the work with deep data structure easier by providing a set of safe reader and writer methods.

* def read_target(target, keychain: tuple, default: any = None)
* def write_dictionary(target_dict: dict, keychain: tuple, value: any)

## Logging

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

Several methods for variable level logging provided.

* def debug(self, message: str, extra=None)
* def info(self, message: str, extra=None)
* def warning(self, message: str, extra=None)
* def error(self, message: str, extra=None)
* def exception(self, message: str, exception: BaseException)
* def critical(self, message: str, extra=None)

The `extra` could be anything, and would be tried to print as JSON encoded string.

The `exception` method is designed for the try block to print the call stack.

## MySQL

See [Nehushtan MySQL Package](./mysql).