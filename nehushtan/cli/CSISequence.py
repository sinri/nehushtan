class CSISequence:
    """
    Since 0.4.13
    """

    def __init__(self, parameter='', intermediate='', final=''):
        """
        CSI序列由ESC [、若干个（包括0个）“参数字节”、若干个“中间字节”，以及一个“最终字节”组成。

        参数字节	0x30–0x3F	0–9:;<=>?
        中间字节	0x20–0x2F	空格、!"#$%&'()*+,-./
        最终字节	0x40–0x7E	@A–Z[\]^_`a–z{|}~

        """

        self.parameter = parameter
        self.intermediate = intermediate
        self.final = final

    def to_string(self):
        return '\033[' + self.parameter + self.intermediate + self.final

    def __str__(self):
        return self.to_string()
