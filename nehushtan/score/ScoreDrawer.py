from typing import List, Optional

from nehushtan.paint.Paint import Paint
from nehushtan.score.ParsedLine import ParsedLine
from nehushtan.score.ParsedLineAsLyric import ParsedLineAsLyric
from nehushtan.score.ParsedLineAsScore import ParsedLineAsScore
from nehushtan.score.ParsedLineAsTitle import ParsedLineAsTitle


class ScoreDrawer:
    def __init__(self,
                 parsed_lines: List[ParsedLine],
                 ttf_font_file_path,
                 font_size: int = 50
                 ):
        self.__parsed_lines = parsed_lines

        self.__ttf_font_file_path = ttf_font_file_path
        self.__font_size = font_size
        self.__font = Paint.load_ttf_font(self.__ttf_font_file_path, self.__font_size)

        self.__line_width = int(max(2.0, self.__font_size / 10))
        self.__point_width = int(max(3.0, self.__font_size / 8))

        self.__max_columns = 0
        self.__max_prefix_columns = 0
        self.__max_score_columns = 0

        self.__compute_cells()

        self.__cell_width = font_size
        self.__cell_height = font_size
        self.__paint: Optional[Paint] = None

        self.__prepare_image_paper()

        self.__draw_lines()

    def show(self, title: Optional[str] = None):
        self.__paint.show(title)

    def __compute_cells(self):
        max_columns = 0
        max_prefix_columns = 0
        max_score_columns = 0
        for line in self.__parsed_lines:
            if isinstance(line, ParsedLineAsTitle):
                total_chars = len(line.get_middle_component())
                if line.get_left_componet() is not None:
                    total_chars += 1 + len(line.get_left_componet())
                if line.get_right_component() is not None:
                    total_chars += 1 + len(line.get_right_component())
                if total_chars > max_columns:
                    max_columns = total_chars
            elif isinstance(line, ParsedLineAsScore):
                # compute for score
                cells = 0
                for su in line.get_score_units():
                    cells += su.get_cell_needed()
                if cells > max_score_columns:
                    max_score_columns = cells
            elif isinstance(line, ParsedLineAsLyric):
                prefix_size = 0
                if line.get_prefix() is not None:
                    prefix_size += len(line.get_prefix())  # + 1

                if prefix_size > max_prefix_columns:
                    max_prefix_columns = prefix_size

                total_chars = 0
                total_chars += len(line.get_content())
                if total_chars > max_columns:
                    max_columns = total_chars

        self.__max_columns = max_columns
        self.__max_prefix_columns = max_prefix_columns
        self.__max_score_columns = max_score_columns

        # print(f"self.__max_columns = {self.__max_columns}")
        # print(f"self.__max_prefix_columns = {self.__max_prefix_columns}")
        # print(f"self.__max_score_columns = {self.__max_score_columns}")

    def __prepare_image_paper(self):
        with Paint(400, 400) as p:
            x = p.textbbox(
                (0, 0),
                "喵",
                self.__font,
                align="center"
            )
            # print(x)
            self.__cell_width = x[2] + 2
            self.__cell_height = int((x[3] + 2) * 1.5)
            # print(f'self.__cell_width={self.__cell_width} self.__cell_height={self.__cell_height}')

        width = self.__max_prefix_columns
        if width > 0:
            width += 1
        width += self.__max_score_columns
        if self.__max_columns > width:
            width = self.__max_columns
        width += 2
        width = width * self.__cell_width

        height = (len(self.__parsed_lines) + 1 + 2) * self.__cell_height

        self.__paint = Paint(width, height, mode="RGB", background_color="white")
        # print(f'width={width} height={height}')

    def __draw_lines(self):
        line_index = 1
        for line in self.__parsed_lines:
            if isinstance(line, ParsedLineAsTitle):
                self.__draw_title_line(line_index, line)
            elif isinstance(line, ParsedLineAsScore):
                self.__draw_score_line(line_index, line)
            elif isinstance(line, ParsedLineAsLyric):
                self.__draw_lyric_line(line_index, line)
            else:
                self.__paint.text(
                    (self.__cell_width, line_index * self.__cell_height),
                    "不支持的 PARSED LINE",
                    font=self.__font,
                    align="center"
                )

            line_index += 1

    def __draw_title_line(self, line_index: int, title_line: ParsedLineAsTitle):
        if title_line.get_left_componet() is not None:
            box = self.__paint.textbbox(
                xy=(0, 0),
                text=title_line.get_left_componet(),
                font=self.__font,
                align="left"
            )
            self.__paint.text(
                xy=(self.__cell_width, line_index * self.__cell_height),
                text=title_line.get_left_componet(),
                font=self.__font,
                align="left",
                fill="black"
            )
        if title_line.get_middle_component() is not None:
            box = self.__paint.textbbox(
                xy=(0, 0),
                text=title_line.get_middle_component(),
                font=self.__font,
                align="center"
            )
            self.__paint.text(
                xy=(
                    self.__paint.get_image().width / 2 - box[2] / 2,
                    line_index * self.__cell_height
                ),
                text=title_line.get_middle_component(),
                font=self.__font,
                align="center",
                fill="black",
            )
        if title_line.get_right_component() is not None:
            box = self.__paint.textbbox(
                xy=(0, 0),
                text=title_line.get_right_component(),
                font=self.__font,
                align="right"
            )
            xy = (
                self.__paint.get_image().width - self.__cell_width * 1 - box[2],
                line_index * self.__cell_height
            )
            self.__paint.text(
                xy=xy,
                text=title_line.get_right_component(),
                font=self.__font,
                align="right",
                fill="black"
            )

    def __draw_score_line(self, line_index: int, score_line: ParsedLineAsScore):
        cell_index = 1
        if self.__max_prefix_columns > 0:
            cell_index += self.__max_prefix_columns + 1

        in_tie_or_slur = False
        ts_start_cell_index = None
        ts_end_cell_index = None
        ts_above_y = None

        for i in range(len(score_line.get_score_units())):
            su = score_line.get_score_unit(i)
            print(f"draw su: {su}")

            # draw su
            note = su.get_note()
            if note == "(":
                in_tie_or_slur = True
                ts_start_cell_index = cell_index
                ts_above_y = None
                continue
            elif note == ")":
                in_tie_or_slur = False
                ts_end_cell_index = cell_index
                # draw tie or clur
                self.aimed_tie_or_slur(
                    (ts_start_cell_index * self.__cell_width, ts_above_y),
                    (ts_end_cell_index * self.__cell_width, ts_above_y),
                    int(max(5.0, self.__cell_height * 0.2)),
                    "black"
                )
                continue
            elif note == ")3":
                in_tie_or_slur = False
                ts_end_cell_index = cell_index
                # draw tie or clur for triplet
                self.aimed_tie_or_slur(
                    (ts_start_cell_index * self.__cell_width, ts_above_y),
                    (ts_end_cell_index * self.__cell_width, ts_above_y),
                    int(max(5.0, self.__cell_height * 0.2)),
                    "black"
                )
                small_font = Paint.load_ttf_font(self.__ttf_font_file_path, int(self.__font_size * 2 / 3.0))
                self.aimed_text(
                    int((ts_start_cell_index + ts_end_cell_index) / 2 * self.__cell_width),
                    int(ts_above_y - max(5.0, self.__cell_height * 0.2) - 2),
                    "3",
                    small_font,
                    "black",
                    background_color="white"
                )
                continue
            elif note in ("|", "||", "||:", ":||", "|:", ":|"):
                self.aimed_text(
                    int((cell_index + 0.5) * self.__cell_width),
                    int((line_index + 0.5) * self.__cell_height),
                    text=note,
                    font=self.__font,
                    fill="black"
                )
                cell_index += 1
            else:
                # 0, 1-7
                self.aimed_text(
                    int((cell_index + 0.5) * self.__cell_width),
                    int((line_index + 0.5) * self.__cell_height),
                    text=note,
                    font=self.__font,
                    fill="black"
                )
                under_line_start_cell_index = cell_index
                if su.get_right_line_count() > 0:
                    for right_line_index in range(su.get_right_line_count()):
                        cell_index += 1
                        self.aimed_text(
                            int((cell_index + 0.5) * self.__cell_width),
                            int((line_index + 0.5) * self.__cell_height),
                            text="-",
                            font=self.__font,
                            fill="black"
                        )
                if su.get_dot():
                    cell_index += 1
                    self.aimed_point(
                        int((cell_index + 0.5) * self.__cell_width),
                        int((line_index + 0.5) * self.__cell_height),
                        self.__point_width,
                        "black"
                    )
                    # self.aimed_text(
                    #     int((cell_index + 0.5) * self.__cell_width),
                    #     int((line_index + 0.5) * self.__cell_height),
                    #     text="·",
                    #     font=self.__font,
                    #     fill="black"
                    # )
                under_line_end_cell_index = cell_index

                under_y = int((line_index + 1 - 0.1) * self.__cell_height)
                if su.get_under_line_count() > 0:
                    x0 = under_line_start_cell_index * self.__cell_width
                    x1 = (under_line_end_cell_index + 1) * self.__cell_width
                    for under_line_index in range(su.get_under_line_count()):
                        self.__paint.line(
                            xy=(
                                (x0, under_y), (x1, under_y)
                            ),
                            fill="black",
                            width=self.__line_width
                        )
                        under_y += self.__line_width * 2
                if su.get_below_point_count() > 0:
                    for below_point_index in range(su.get_below_point_count()):
                        self.aimed_point(
                            int((under_line_start_cell_index + 0.5) * self.__cell_width),
                            under_y,
                            self.__point_width,
                            "black"
                        )
                        # self.__paint.ellipse(
                        #     xy=(
                        #         (int((under_line_start_cell_index + 0.5) * self.__cell_width - 1), under_y - 1),
                        #         (int((under_line_start_cell_index + 0.5) * self.__cell_width + 1), under_y + 1)
                        #     ),
                        #     fill="black"
                        # )
                        under_y += self.__point_width * 2

                above_y = int((line_index + 0.25) * self.__cell_height)
                if su.get_above_point_count() > 0:
                    for above_point_index in range(su.get_above_point_count()):
                        # self.__paint.ellipse(
                        #     xy=(
                        #         (int((under_line_start_cell_index + 0.5) * self.__cell_width - 1), above_y - 1),
                        #         (int((under_line_start_cell_index + 0.5) * self.__cell_width + 1), above_y + 1)
                        #     ),
                        #     fill="black"
                        # )
                        self.aimed_point(
                            int((under_line_start_cell_index + 0.5) * self.__cell_width),
                            above_y,
                            self.__point_width,
                            "black"
                        )
                        above_y -= self.__point_width * 2

                if su.get_fermata():
                    self.aimed_fermata(
                        int((under_line_start_cell_index + 0.5) * self.__cell_width),
                        above_y,
                        "black"
                    )
                    above_y = above_y - self.__cell_width / 3 - self.__point_width

                if in_tie_or_slur:
                    if ts_above_y is None or ts_above_y > above_y:
                        ts_above_y = above_y

                cell_index += 1

    def __draw_lyric_line(self, line_index: int, lyric_line: ParsedLineAsLyric):
        lyric_body_offset = self.__cell_width
        if self.__max_prefix_columns > 0:
            if lyric_line.get_prefix() is not None:
                box = self.__paint.textbbox(
                    xy=(0, 0),
                    text=lyric_line.get_prefix(),
                    font=self.__font,
                    align="right"
                )
                self.__paint.text(
                    xy=(
                        self.__cell_width * (1 + self.__max_prefix_columns) - box[2],
                        line_index * self.__cell_height
                    ),
                    text=lyric_line.get_prefix(),
                    font=self.__font,
                    align="right",
                    fill="black"
                )

            lyric_body_offset += (self.__max_prefix_columns + 1) * self.__cell_width

        for i in range(len(lyric_line.get_content())):
            self.__paint.text(
                xy=(
                    lyric_body_offset + i * self.__cell_width,
                    line_index * self.__cell_height
                ),
                text=lyric_line.get_lyric_char(i),
                font=self.__font,
                align="center",
                fill="black"
            )

    def aimed_text(self, center_x, center_y, text, font, fill="black", background_color=None):
        box = self.__paint.textbbox(
            xy=(0, 0),
            text=text,
            font=font,
            align="center"
        )
        x = int(center_x - box[2] / 2)
        y = int(center_y - box[3] / 2)

        if background_color is not None:
            self.__paint.rectangle(
                ((x, y), (x + box[2], y + box[3])),
                fill=background_color
            )

        self.__paint.text(
            xy=(x, y),
            text=text,
            fill=fill,
            font=font,
            align="center"
        )

    def aimed_point(self, center_x, center_y, width: int = 3, fill="black"):
        self.__paint.ellipse(
            xy=(
                (int(center_x - width / 2), int(center_y - width / 2)),
                (int(center_x + width / 2), int(center_y + width / 2)),
            ),
            fill=fill,
            width=width
        )

    def aimed_fermata(self, point_x, point_y, fill="black"):
        # self.__paint.rectangle(
        #     (
        #         (point_x - self.__cell_width / 3, point_y - self.__cell_width / 3),
        #         (point_x + self.__cell_width / 3, point_y)
        #     ),
        #     outline="red"
        # )
        self.__paint.arc(
            (
                (point_x - self.__cell_width / 3, point_y - self.__cell_width / 3),
                (point_x + self.__cell_width / 3, point_y)
            ),
            180,
            0,
            fill=fill,
            width=self.__point_width
        )
        self.aimed_point(point_x, int(point_y - self.__cell_width / 12), self.__point_width, fill)

    def aimed_tie_or_slur(self, start_xy, end_xy, high, fill="black"):
        self.__paint.arc(
            (
                (start_xy[0], int(start_xy[1] - high)),
                (end_xy[0], end_xy[1])
            ),
            # 225,315,
            180, 0,
            fill=fill,
            width=self.__line_width
        )
