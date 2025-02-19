import unittest
from pixel_map import Pixel, Map


class TestPixelMap(unittest.TestCase):
    def setUp(self):
        self.map = Map(width=10, height=10)
        self.test_position = (1, 2)
        self.pixel = Pixel(position=self.test_position)

    def test_get_pixel_returns_correct_pixel(self):
        self.map.add_pixel(self.pixel)
        found_pixel = self.map.get_pixel(position=self.test_position)
        self.assertEqual(found_pixel, self.pixel)

    def test_get_pixel_returns_none_when_not_found(self):
        non_existent_position = (3, 4)
        found_pixel = self.map.get_pixel(position=non_existent_position)
        self.assertIsNone(found_pixel)

    def test_add_pixel_raises_error_when_outside_bounds(self):
        outside_position = (10, 10)
        with self.assertRaises(ValueError):
            self.map.add_pixel(Pixel(position=outside_position))



if __name__ == '__main__':
    unittest.main()
