# Nehushtan 

A set of Python Toolkits

## CLI 

Class `NehushtanArgumentParser` can parse command line arguments to dict.

`python3 any.py -s a --long b --prefix-c d`

would be finally parsed into 

```
{"s":"a","long":"b","prefix":{"c":"d"}}
```
