import math
from typing import Union

from nehushtan.wave.Note import Note
from nehushtan.wave.WaveWriter import WaveWriter


class SimpleComposer:
    def __init__(self, target_wav_file_path: str, beats_in_minute: int = 96):
        self.__wave_writer = WaveWriter(target_wav_file_path)
        self.__beats_in_minute = beats_in_minute

        self.__note_frames_cache = []

    def add_note(self, note: Note):
        self.__add_sound(int(note.get_sound_in_hz()), note.beats)

    def __add_sound(self, frequency_in_hz: int, beats: Union[int, float]):
        # make time piece
        # 每次采样代表的秒数 = 1秒 / 每秒采样次数
        step = 1.0 / self.__wave_writer.get_frame_rate()
        # 本音占用时长 = 拍数 * (一分钟 / 每分钟拍数)
        time = beats * 60.0 / self.__beats_in_minute
        piece_count = int(round(time / step))

        print(f"time={time},piece_count={piece_count}")

        frames = []
        for i in range(piece_count):
            t = step * i
            frame = math.cos(2 * math.pi * (frequency_in_hz * t)) * 10000
            frames.append(int(frame))

        self.__note_frames_cache.append(frames)
        # print(frames)
        # self.__wave_writer.write_frames(frames)

    def close(self):
        last = None
        total = []
        for frames in self.__note_frames_cache:
            if last is not None:
                first = frames[0]

                middle_beats = 10
                delta = 1.0 * (first - last) / middle_beats
                for i in range(middle_beats):
                    x = last + i * delta
                    total.append(int(x))

            total = total + frames
            last = total[-1]
        self.__wave_writer.write_frames(total)
        self.__wave_writer.close()
