from dataclasses import dataclass
from typing import List


@dataclass
class Pixel:
    position: tuple[int, int]


class Map:
    def __init__(self, width: int, height: int):
        self.pixels: List[Pixel] = []
        self.width = width
        self.height = height

    def add_pixel(self, pixel: Pixel):
        x, y = pixel.position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels.append(pixel)
        else:
            raise ValueError(f"Pixel position {pixel.position} is outside map bounds")

    def get_pixel(self, position: tuple[int, int]) -> Pixel:
        return next((pixel for pixel in self.pixels if pixel.position == position), None)
