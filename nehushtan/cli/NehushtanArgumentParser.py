import re
import sys


class NehushtanArgumentParser:
    """
    Support
    <python xxx.py> [-a B] [--bb C] [--dd-ee F --dd-gg H]
    Parsed as
    {
        "a":"B"
        "bb":"C",
        "dd":{
            "ee":"F",
            "gg":"H",
        }
    }
    """

    def __init__(self, sys_arg_list: list = None):
        """
        Since 0.2.19 sys_arg_list become optional
        :param sys_arg_list: a list of arguments, if omitted use `sys.argv[1:]`
        """
        if sys_arg_list is None:
            sys_arg_list = sys.argv[1:]

        self._sys_arg_list = sys_arg_list
        self._argument_dict = {}
        self._options_short = {}
        self._options_long = {}
        self._options_prefix = {}
        self._result_dict = {}
        self._usage_dict = {}

    def set_arg_list(self, arg_list: list):
        """
        :param arg_list: Commonly `sys.argv[1:]`
        """
        self._sys_arg_list = arg_list
        return self

    def add_option(self, key: str, desc: str = '', short: str = '', long: str = '', prefix: str = ''):
        """

        :param desc:
        :param key: Any Name
        :param short: a -> `-a`
        :param long: alpha -> `--alpha`
        :param prefix: alef -> `--alef-`
        :return:
        """
        if short == '' and long == '' and prefix == '':
            return self

        usage = {
            'key': key,
            'desc': desc,
        }
        if short != '':
            argument_key = f'-{short}'
            if self._options_short.get(argument_key) is not None:
                raise RuntimeError(f'Short Key [{argument_key}] Already Existed')
            self._options_short[argument_key] = key
            usage['short'] = f'-{short} [VALUE]'
        if long != '':
            argument_key = f'--{long}'
            if self._options_long.get(argument_key) is not None:
                raise RuntimeError(f'Long Key [{argument_key}] Already Existed')
            self._options_long[argument_key] = key
            usage['long'] = f'--{long} [VALUE]'
        if prefix != '':
            argument_key = f'--{prefix}-'
            if self._options_prefix.get(argument_key) is not None:
                raise RuntimeError(f'Prefix Key [{argument_key}] Already Existed')
            self._options_prefix[argument_key] = key
            usage['prefix'] = f'--{prefix}-[KEY] [VALUE]'

        self._usage_dict[key] = usage

        return self

    def parse(self):
        current_key = None
        self._argument_dict = {}
        for item in self._sys_arg_list:
            if current_key is None:
                current_key = item
            else:
                self._argument_dict[current_key] = item
                current_key = None

        self._result_dict = {}
        for (key, value) in self._argument_dict.items():
            if self._options_short.get(key) is not None:
                self._result_dict[self._options_short[key]] = value
            elif self._options_long.get(key) is not None:
                self._result_dict[self._options_long[key]] = value
            else:
                for prefix, mapping_key in self._options_prefix.items():
                    matches = re.match(f'^{prefix}([A-Za-z0-9._-]+)$', key)
                    if matches is not None:
                        if self._result_dict.get(mapping_key) is None:
                            self._result_dict[mapping_key] = {}
                        self._result_dict[mapping_key][matches[1]] = value
                        break
        return self

    def get_raw_option_dict(self):
        return self._argument_dict

    def get_parsed_option_dict(self):
        return self._result_dict

    def get_usage_text(self):
        usage_text = ""
        for key, value in self._usage_dict.items():
            options = []
            if len(value.get('short', '')) > 0:
                options.append(value.get('short'))
            if len(value.get('long', '')) > 0:
                options.append(value.get('long'))
            if len(value.get('prefix', '')) > 0:
                options.append(value.get('prefix'))

            usage_text += f"{value['key']}" + "\t\t"
            usage_text += ", ".join(options)
            if len(value.get('desc', '')) > 0:
                usage_text += f"\n{value['desc']}"
            usage_text += "\n"

        return usage_text


if __name__ == '__main__':
    print(NehushtanArgumentParser().add_option('A', 'argument A', 'a').parse().get_parsed_option_dict())
