# Nehushtan Command Line Toolkit

## Argument Parser 

Class `NehushtanArgumentParser` can parse command line arguments to dict.

`python3 any.py -s a --long b --prefix-c d`

would be finally parsed into 

```
{"s":"a","long":"b","prefix":{"c":"d"}}
```

----

Back to [index](./index)