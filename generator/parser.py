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
        self._move_point_rnd = move_point_rnd
        self._painter = Painter("BMP", paint_chance_rnd=paint_chance_rnd)

    def parse(self):
        lines = self._get_text_lines()
        tags = []
        for line in lines:
            t = None
            if line.split()[0].lower() == Point.kPoint:
                t = Point.parse(line)
            elif line.split()[0].lower() == Line.kLine:
                t = Line.parse(line)
            elif line.split()[0].lower() == Bezier.kBezier:
                t = Bezier.parse(line)
            elif line.split()[0].lower() == Circle.kCircle:
                t = Circle.parse(line)
            elif line.split()[0].lower() == ConnectLeft.kConnectLeft:
                t = ConnectLeft.parse(line)
            elif line.split()[0].lower() == ConnectRight.kConnectRight:
                t = ConnectRight.parse(line)
            else:
                Logger().error("Wrong token name!")
            Logger().debug(t)
            tags.append(t)
        self._get_points(tags)
        self._get_lines(tags)

    def paint(self):
        self._random_points(self._move_point_rnd)
        for line in self._lines:
            self._painter.line(self._points[line.name_a],
                               self._points[line.name_b])

    def _random_points(self, randomness):
        for point in self._points:
            self._points[point].x += random.randint(-randomness, randomness)
            self._points[point].y += random.randint(-randomness, randomness)

    def _get_points(self, tags):
        for tag in tags:
            if type(tag) == Point:
                self._points[tag.name] = tag

    def _get_lines(self, tags):
        for tag in tags:
            if type(tag) == Line:
                self._lines.append(tag)

    def _get_text_lines(self):
        with open(self._file_name) as in_file:
            return in_file.readlines()
