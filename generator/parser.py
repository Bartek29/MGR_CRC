from common.logger import Logger
from generator.key_words import Bezier
from generator.key_words import Circle
from generator.key_words import ConnectLeft
from generator.key_words import ConnectRight
from generator.key_words import Line
from generator.key_words import Point


class Parser(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self.points = {}

    def parse(self):
        lines = self._get_lines()
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

    def _get_points(self, tags):
        for tag in tags:
            if type(tag) == Point:
                self.points[tag.name] = tag

    def _get_lines(self):
        with open(self._file_name) as in_file:
            return in_file.readlines()
