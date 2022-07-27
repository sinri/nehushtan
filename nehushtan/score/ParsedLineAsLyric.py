import json

from nehushtan.score.ParsedLine import ParsedLine


class ParsedLineAsLyric(ParsedLine):
    def __init__(self, content: str, prefix=None):
        super().__init__()
        self.__prefix = prefix
        self.__content = content

    def get_prefix(self):
        return self.__prefix

    def get_content(self):
        return self.__content

    def get_lyric_char(self, index: int):
        return self.__content[index]

    def __str__(self):
        x = (self.__prefix, self.__content)
        return "ParsedLineAsLyric: " + json.dumps(x)
