import random

from common.logger import Logger
from generator.key_words import Bezier
from generator.key_words import Circle
from generator.key_words import ConnectLeft
from generator.key_words import ConnectRight
from generator.key_words import Line
from generator.key_words import Point
from generator.painter import Painter


class Parser(object):
    def __init__(self, file_name, move_point_rnd=0, paint_chance_rnd=1.0):
        self._file_name = file_name
        self._points = {}
        self._lines = []
        self._bezier = []
        self._move_point_rnd = move_point_rnd
        self._painter = Painter("BMP", paint_chance_rnd=paint_chance_rnd)

    def parse(self):
        lines = self._get_text_lines()
        for line in lines:
            if line.split()[0].lower() == Point.kPoint:
                t = Point.parse(line)
                self._points[t.name] = t
            elif line.split()[0].lower() == Line.kLine:
                self._lines.append(Line.parse(line))
            elif line.split()[0].lower() == Bezier.kBezier:
                self._bezier.append(Bezier.parse(line))
            elif line.split()[0].lower() == Circle.kCircle:
                t = Circle.parse(line)
            elif line.split()[0].lower() == ConnectLeft.kConnectLeft:
                t = ConnectLeft.parse(line)
            elif line.split()[0].lower() == ConnectRight.kConnectRight:
                t = ConnectRight.parse(line)
            else:
                Logger().error("Wrong token name!")

    def paint(self):
        self._random_points(self._move_point_rnd)
        for line in self._lines:
            self._painter.line(self._points[line.name_a],
                               self._points[line.name_b])
        for bezier in self._bezier:
            self._painter.bezier(self._points[bezier.name_a],
                                 self._points[bezier.name_b],
                                 self._points[bezier.name_c],
                                 self._points[bezier.name_d])
        self._painter.write("test.bmp")

    def _random_points(self, randomness):
        for point in self._points:
            self._points[point].x += random.randint(-randomness, randomness)
            self._points[point].y += random.randint(-randomness, randomness)

    def _get_text_lines(self):
        with open(self._file_name) as in_file:
            return in_file.readlines()
