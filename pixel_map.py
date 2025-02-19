from dataclasses import dataclass
from typing import List


@dataclass
class Pixel:
    position: tuple[int, int]
    id: int = 0


class Map:
    def __init__(self, width: int, height: int):
        self.pixels: List[Pixel] = []
        self.width = width
        self.height = height
        self._next_id = 1

    def add_pixel(self, pixel: Pixel):
        x, y = pixel.position
        if 0 <= x < self.width and 0 <= y < self.height:
            pixel.id = self._next_id
            self._next_id += 1
            self.pixels.append(pixel)
        else:
            raise ValueError(f"Pixel position {pixel.position} is outside map bounds")

    def get_pixel(self, position: tuple[int, int]) -> Pixel:
        return next((pixel for pixel in self.pixels if pixel.position == position), None)

    def move_pixel_left(self, pixel: Pixel) -> bool:
        if pixel not in self.pixels:
            return False
        
        x, y = pixel.position
        new_position = (x - 1, y)
        
        if x - 1 >= 0 and not self.get_pixel(new_position):
            pixel.position = new_position
            return True
        return False

    def move_pixel_right(self, pixel: Pixel) -> bool:
        if pixel not in self.pixels:
            return False
        
        x, y = pixel.position
        new_position = (x + 1, y)
        
        if x + 1 < self.width and not self.get_pixel(new_position):
            pixel.position = new_position
            return True
        return False

    def move_pixel_up(self, pixel: Pixel) -> bool:
        if pixel not in self.pixels:
            return False
        
        x, y = pixel.position
        new_position = (x, y - 1)
        
        if y - 1 >= 0 and not self.get_pixel(new_position):
            pixel.position = new_position
            return True
        return False

    def move_pixel_down(self, pixel: Pixel) -> bool:
        if pixel not in self.pixels:
            return False
        
        x, y = pixel.position
        new_position = (x, y + 1)
        
        if y + 1 < self.height and not self.get_pixel(new_position):
            pixel.position = new_position
            return True
        return False
