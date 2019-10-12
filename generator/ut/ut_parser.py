import unittest

from generator.key_words import Line
from generator.key_words import Point


class TestPoint(unittest.TestCase):
    def test_good(self):
        point_txt = "point A 0 0"
        test_point = Point.parse(point_txt)

        point = Point("A", 0, 0)

        self.assertEqual(point.name, test_point.name)
        self.assertEqual(point.x, test_point.x)
        self.assertEqual(point.y, test_point.y)

    def test_wrong_tag_name(self):
        point_txt = "poant A 0 0"
        self.assertRaises(ValueError, Point.parse, point_txt)

    def test_wrong_number_of_tokens_3(self):
        point_txt = "point A 0"
        self.assertRaises(ValueError, Point.parse, point_txt)

    def test_wrong_number_of_tokens_5(self):
        point_txt = "point A 0 0 0"
        self.assertRaises(ValueError, Point.parse, point_txt)

    def test_float_point(self):
        point_txt = "point A 1.4 3.5"
        self.assertRaises(ValueError, Point.parse, point_txt)


class TestLine(unittest.TestCase):
    def test_good(self):
        line_txt = "line A B"
        test_line = Line.parse(line_txt)

        line = Line("A", "B")

        self.assertEqual(line.name_a, test_line.name_a)
        self.assertEqual(line.name_b, test_line.name_b)

    def test_wrong_tag_name(self):
        line_txt = "liasdne A B"
        self.assertRaises(ValueError, Line.parse, line_txt)

    def test_wrong_number_of_tokens_2(self):
        line_txt = "line A"
        self.assertRaises(ValueError, Line.parse, line_txt)

    def test_wrong_number_of_tokens_4(self):
        line_txt = "line A B C"
        self.assertRaises(ValueError, Line.parse, line_txt)
