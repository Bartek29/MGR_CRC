import unittest

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
