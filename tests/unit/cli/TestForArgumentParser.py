import unittest

from nehushtan.cli.NehushtanArgumentParser import NehushtanArgumentParser


class TestForArgumentParser(unittest.TestCase):

    def test_for_parse(self):
        parser = NehushtanArgumentParser(['-a', 'aa', '--dd', 'ee', '--gg-hh', 'ii', 'j', 'k']) \
            .add_option('A', 'arg A', short='a') \
            .add_option('D', 'arg D', long='dd') \
            .add_option('G', 'arg G', prefix='gg') \
            .parse()

        parsed = parser.get_parsed_option_dict()
        expected = {'A': 'aa', 'D': 'ee', 'G': {'hh': 'ii'}}
        self.assertEqual(expected, parsed)

    def test_for_later_parse(self):
        try:
            NehushtanArgumentParser() \
                .add_option('A', 'arg A', short='a') \
                .add_option('D', 'arg D', short='a', long='dd') \
                .add_option('G', 'arg G', prefix='gg') \
                .set_arg_list(['-a', 'aa', '--dd', 'ee', '--gg-hh', 'ii', 'j', 'k']) \
                .parse()
        except RuntimeError as e:
            self.assertEqual('Short Key [-a] Already Existed', e.__str__())
        else:
            self.fail('Did not seek out the duplicated key')
