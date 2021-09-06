import re
from typing import Union

from nehushtan.cli.CSISequence import CSISequence


class ANSITermialHelper:
    """
    Since 0.4.13
    """

    # SGR (Select Graphic Rendition) Parameters

    SGR_RESET = 0
    SGR_BOLD = 1
    SGR_FAINT = 2  # 未广泛支持。
    SGR_ITALIC = 3  # 未广泛支持。有时视为反相显示。
    SGR_UNDERLINE = 4
    SGR_SLOW_BLINK = 5
    SGR_RAPID_BLINK = 6  # MS-DOS ANSI.SYS；每分钟150以上；未广泛支持。
    SGR_INVERT = 7
    SGR_HIDE = 8  # 未广泛支持。
    SGR_STRIKE = 9  # 未广泛支持。

    SGR_USE_DEFAULT_FONT = 10
    SGR_USE_FONT_1 = 11
    SGR_USE_FONT_2 = 12
    SGR_USE_FONT_3 = 13
    SGR_USE_FONT_4 = 14
    SGR_USE_FONT_5 = 15
    SGR_USE_FONT_6 = 16
    SGR_USE_FONT_7 = 17
    SGR_USE_FONT_8 = 18
    SGR_USE_FONT_9 = 19
    SGR_BLACKLETTER_FONT = 20  # 几乎无支持。

    SGR_DOUBLY_UNDERLINED = 21
    SGR_NOT_BOLD = 21

    SGR_NORMAL_INTENSITY = 22  # 正常颜色或强度
    SGR_NEITHER_ITALIC_NOR_BLACKLETTER = 23  # 非斜体、非尖角体
    SGR_NOT_UNDERLINED = 24  # 关闭下划线	去掉单双下划线。
    SGR_NOT_BLINKING = 25  # 关闭闪烁
    SGR_NOT_REVERSED = 27  # 关闭反显
    SGR_REVEAL = 28  # 关闭隐藏
    SGR_NOT_STRIKE = 29  # 关闭划除

    # 30–37	设置前景色	参见下面的颜色表。
    # 38	设置前景色	下一个参数是5;n或2;r;g;b，见下。
    # 39	默认前景色	由具体实现定义（按照标准）。

    SGR_SET_FOREGROUND_COLOR = 38

    SGR_FOREGROUND_COLOR_BLACK = 30
    SGR_FOREGROUND_COLOR_RED = 31
    SGR_FOREGROUND_COLOR_GREEN = 32
    SGR_FOREGROUND_COLOR_YELLOW = 33
    SGR_FOREGROUND_COLOR_BLUE = 34
    SGR_FOREGROUND_COLOR_MAGENTA = 35
    SGR_FOREGROUND_COLOR_CYAN = 36
    SGR_FOREGROUND_COLOR_WHITE = 37

    SGR_DEFAULT_FOREGROUND_COLOR = 39

    # 40–47	设置背景色	参见下面的颜色表。
    # 48	设置背景色	下一个参数是5;n或2;r;g;b，见下。
    # 49	默认背景色	由具体实现定义（按照标准）。

    SGR_Set_background_color = 48

    SGR_BACKGROUND_COLOR_BLACK = 40
    SGR_BACKGROUND_COLOR_RED = 41
    SGR_BACKGROUND_COLOR_GREEN = 42
    SGR_BACKGROUND_COLOR_YELLOW = 43
    SGR_BACKGROUND_COLOR_BLUE = 44
    SGR_BACKGROUND_COLOR_MAGENTA = 45
    SGR_BACKGROUND_COLOR_CYAN = 46
    SGR_BACKGROUND_COLOR_WHITE = 47

    SGR_DEFAULT_background_COLOR = 49

    # Implemented as "emoji variation selector" in mintty.
    # see https://github.com/mintty/mintty/wiki/Tips#text-attributes-and-rendering
    SGR_FRAMED = 51
    SGR_ENCIRCLED = 52
    SGR_NOT_FRAMED_OR_ENCIRCLED = 54

    SGR_OVERLINED = 53  # 上划线
    SGR_NOT_OVERLINED = 55  # 关闭上划线

    def __init__(self):
        pass

    # @staticmethod
    # def csi_string(parameter='', intermediate='', final=''):
    #     """
    #     CSI序列由ESC [、若干个（包括0个）“参数字节”、若干个“中间字节”，以及一个“最终字节”组成。
    #
    #     参数字节	0x30–0x3F	0–9:;<=>?
    #     中间字节	0x20–0x2F	空格、!"#$%&'()*+,-./
    #     最终字节	0x40–0x7E	@A–Z[\]^_`a–z{|}~
    #
    #     """
    #     return '\033[' + parameter + intermediate + final

    # @staticmethod
    # def write_csi_string():
    #     print()

    @staticmethod
    def write(text: Union[str, CSISequence], end: str = ''):
        # if type(text) is not str:
        #     print('<CSI-DEBUG>'+text.__str__()+'</CSI-DEBUG>')
        print(text.__str__(), end=end, flush=True)

    # 光标向指定的方向移动{\displaystyle n}n（默认1）格。如果光标已在屏幕边缘，则无效。

    def cursor_up(self, n: int = 1):
        self.write(CSISequence(f'{n}', '', 'A'))

    def cursor_down(self, n: int = 1):
        self.write(CSISequence(f'{n}', '', 'B'))

    def cursor_forward(self, n: int = 1):
        self.write(CSISequence(f'{n}', '', 'C'))

    def cursor_back(self, n: int = 1):
        self.write(CSISequence(f'{n}', '', 'D'))

    def cursor_next_line(self, n: int = 1):
        """
        光标移动到下面第 n（默认1）行的开头。（非ANSI.SYS）
        """
        self.write(CSISequence(f'{n}', '', 'E'))

    def cursor_previous_line(self, n: int = 1):
        """
        光标移动到上面第 n（默认1）行的开头。（非ANSI.SYS）
        """
        self.write(CSISequence(f'{n}', '', 'F'))

    def cursor_horizontal_absolute(self, n: int = 1):
        """
        光标移动到第 n（默认1）列。（非ANSI.SYS）
        """
        self.write(CSISequence(f'{n}', '', 'G'))

    def cursor_move_to_position(self, row_number: int = 1, column_number: int = 1):
        """
        光标移动到第 row_number 行、第 column_number 列。
        值从1开始，且默认为1（左上角）。
        例如CSI ;5H和CSI 1;5H含义相同；
        CSI 17;H、CSI 17H和CSI 17;1H三者含义相同。
        """
        self.write(CSISequence(f'{row_number};{column_number}', '', 'H'))

    def cursor_format_to_position(self, row_number: int = 1, column_number: int = 1):
        """
        Horizontal Vertical Position
        Same as CUP, but counts as a format effector function (like CR or LF)
            rather than an editor function (like CUD or CNL).
        This can lead to different handling in certain terminal modes.
        """
        self.write(CSISequence(f'{row_number};{column_number}', '', 'f'))

    def erase_area(self, n: int = 0):
        """
        清除屏幕的部分区域。
        如果n是0（或缺失），则清除从光标位置到屏幕末尾的部分。
        如果n是1，则清除从光标位置到屏幕开头的部分。
        如果n是2，则清除整个屏幕（在DOS ANSI.SYS中，光标还会向左上方移动）。
        如果n是3，则清除整个屏幕，并删除回滚缓存区中的所有行（这个特性是xterm添加的，其他终端应用程序也支持）。
        """
        self.write(CSISequence(f'{n}', '', 'J'))

    def erase_area_future(self):
        """
        清除从光标位置到屏幕末尾的部分
        """
        self.erase_area(0)

    def erase_area_past(self):
        """
        清除从光标位置到屏幕开头的部分
        """
        self.erase_area(1)

    def erase_area_all(self):
        """
        清除整个屏幕（在DOS ANSI.SYS中，光标还会向左上方移动）
        """
        self.erase_area(2)

    def erase_area_all_and_clean_buffer(self):
        """
        清除整个屏幕，并删除回滚缓存区中的所有行
        （这个特性是xterm添加的，其他终端应用程序也支持）
        """
        self.erase_area(3)

    def erase_line(self, n: int = 0):
        """
        清除行内的部分区域。
        如果n是0（或缺失），清除从光标位置到该行末尾的部分。
        如果n是1，清除从光标位置到该行开头的部分。
        如果n是2，清除整行。光标位置不变。
        """
        self.write(CSISequence(f'{n}', '', 'K'))

    def erase_line_after(self):
        """
        清除从光标位置到该行末尾的部分
        """
        self.erase_line(0)

    def erase_line_before(self):
        """
        清除从光标位置到该行开头的部分
        """
        self.erase_line(1)

    def erase_line_all(self):
        """
        清除整行。光标位置不变
        """
        self.erase_line(2)

    def scroll_up(self, n: int = 1):
        """
        整页向上滚动n（默认1）行。新行添加到底部。（非ANSI.SYS）
        """
        self.write(CSISequence(f'{n}', '', 'S'))

    def scroll_down(self, n: int = 1):
        """
        整页向下滚动n（默认1）行。新行添加到顶部。（非ANSI.SYS）
        """
        self.write(CSISequence(f'{n}', '', 'T'))

    def select_graphic_redition(self, parameters: list = None):
        """
        选择图形再现（Select Graphic Rendition）
        """
        csi = CSISequence(';'.join(parameters), '', 'm')
        self.write(csi)

    def device_status_report(self):
        """
        Reports the cursor position (CPR) by transmitting `ESC[n;mR`, where n is the row and m is the column.)
        """
        self.write(CSISequence('6', '', 'n'))

    @staticmethod
    def parse_device_status_report():
        """
        read for the response of `device_status_report`
        """
        x = input()
        matches = re.match(r'\033\[(\d+);(\d+)R', x)
        if matches:
            return matches.group(1), matches.group(2)
        else:
            raise IOError(f'Expected `ESC[n;mR` but `{x}` read.')
