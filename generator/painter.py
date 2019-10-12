import random

from abc import ABC, abstractmethod
from struct import pack

from common.logger import Logger
from generator.key_words import Point


class Painter(object):
    def __init__(self, canvas, paint_chance_rnd=1.0):
        self._canvas = {
            "Dummy": DummyCanvas(),
            "BMP": BMPCanvas(100, 100, paint_chance_rnd)
        }[canvas]

    def write(self, file_name):
        self._canvas.write(file_name)

    def bezier(self, p1: Point, p2: Point, p3: Point, p4: Point):
        u = 0.0
        while u <= 1.0:
            xu = pow(1.0 - u, 3) * float(p1.x) + \
                 3.0 * u * pow(1.0 - u, 2) * float(p2.x) + \
                 3.0 * pow(u, 2) * (1.0 - u) * float(p3.x) + \
                 pow(u, 3) * float(p4.x)
            yu = pow(1.0 - u, 3) * float(p1.y) + \
                 3.0 * u * pow(1.0 - u, 2) * float(p2.y) + \
                 3.0 * pow(u, 2) * (1.0 - u) * float(p3.y) + \
                 pow(u, 3) * float(p4.y)
            self._canvas.paint_dot(int(xu), int(yu))
            u += 0.0001

    def line(self, p1: Point, p2: Point):
        if abs(p2.y - p1.y) < abs(p2.x - p1.x):
            if p1.x > p2.x:
                self._line_low(p2.x, p2.y, p1.x, p1.y)
            else:
                self._line_low(p1.x, p1.y, p2.x, p2.y)
        else:
            if p1.y > p2.y:
                self._line_high(p2.x, p2.y, p1.x, p1.y)
            else:
                self._line_high(p1.x, p1.y, p2.x, p2.y)

    def _line_low(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy
        d = 2 * dy - dx
        y = y0

        x = x0
        while x <= x1:
            self._canvas.paint_dot(int(x), int(y))
            if d > 0:
                y = y + yi
                d = d - 2 * dx
            d = d + 2 * dy
            x += 1

    def _line_high(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        d = 2 * dx - dy
        x = x0

        y = y0
        while y <= y1:
            self._canvas.paint_dot(int(x), int(y))
            if d > 0:
                x = x + xi
                d = d - 2 * dy
            d = d + 2 * dx
            y += 1


class ICanvas(ABC):
    @abstractmethod
    def paint_dot(self, x, y, size=1):
        raise NotImplementedError


class DummyCanvas(ICanvas):
    def paint_dot(self, x, y, size=1):
        Logger().info("Dummy paint x[{}] y[{}] s[{}]".format(
            x, y, size))


class BMPCanvas(ICanvas):
    CLR_BLACK = (0, 0, 0)
    CLR_WHITE = (255, 255, 255)

    def __init__(self, width, height, paint_chance_rnd=1.0):
        self._bfType = 19778  # Bitmap signature
        self._bfReserved1 = 0
        self._bfReserved2 = 0
        self._bcPlanes = 1
        self._bcSize = 12
        self._bcBitCount = 24
        self._bfOffBits = 26
        self._bcWidth = width
        self._bcHeight = height
        self._bfSize = 26 + self._bcWidth * 3 * self._bcHeight
        self._graphics = None
        self._paint_chance_rnd = paint_chance_rnd
        self.clear()

    def clear(self):
        self._graphics = [BMPCanvas.CLR_WHITE] * self._bcWidth * self._bcHeight

    def paint_dot(self, x, y, size=2):
        x_ = x - size
        while x_ <= x + size:
            y_ = y - size
            while y_ <= y + size:
                if (x - x_) * (x - x_) + (y - y_) * (y - y_) < size * size and \
                        0 <= x_ < 100 and 0 <= y < 100 and \
                        random.uniform(0.0, 1.0) < self._paint_chance_rnd:
                    self._paint_single_dot(x_, y_)
                y_ += 1
            x_ += 1

    def _paint_single_dot(self, x, y):
        color = BMPCanvas.CLR_BLACK
        if isinstance(color, tuple):
            if x < 0 or y < 0 or x > self._bcWidth - 1 or y > self._bcHeight - 1:
                raise ValueError("Coords out of range")
            if len(color) != 3:
                raise ValueError("Color must be a tuple of 3 elems")
            self._graphics[y * self._bcWidth + x] = (color[2], color[1], color[0])
        else:
            raise ValueError("Color must be a tuple of 3 elems")

    def write(self, file):
        with open(file, 'wb') as f:
            f.write(pack('<HLHHL',
                         self._bfType,
                         self._bfSize,
                         self._bfReserved1,
                         self._bfReserved2,
                         self._bfOffBits))  # Writing BITMAPFILEHEADER
            f.write(pack('<LHHHH',
                         self._bcSize,
                         self._bcWidth,
                         self._bcHeight,
                         self._bcPlanes,
                         self._bcBitCount))  # Writing BITMAPINFO
            for px in self._graphics:
                f.write(pack('<BBB', *px))
            for i in range(4 - ((self._bcWidth * 3) % 4) % 4):
                f.write(pack('B', 0))
