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