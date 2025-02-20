import pygame
from pixel_map import Map, Pixel

class PixelDisplay:
    def __init__(self, pixel_map: Map, cell_size: int = 20):
        pygame.init()
        self.pixel_map = pixel_map
        self.cell_size = cell_size
        self.width = (pixel_map.width + pixel_map.height) * cell_size * 1.1
        self.height = (pixel_map.width + pixel_map.height) * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pixel Map")
        self.offset_x = self.width // 2.4
        self.offset_y = self.height // 4
        
    def draw_grid(self):
        for x in range(self.pixel_map.width + 1):
            start_x = (x - 0) * self.cell_size + self.offset_x
            start_y = (x + 0) * (self.cell_size // 2) + self.offset_y
            end_x = (x - self.pixel_map.height) * self.cell_size + self.offset_x
            end_y = (x + self.pixel_map.height) * (self.cell_size // 2) + self.offset_y
            pygame.draw.line(self.screen, (0, 100, 100), (start_x, start_y), (end_x, end_y))

        for y in range(self.pixel_map.height + 1):
            start_x = (0 - y) * self.cell_size + self.offset_x
            start_y = (0 + y) * (self.cell_size // 2) + self.offset_y
            end_x = (self.pixel_map.width - y) * self.cell_size + self.offset_x
            end_y = (self.pixel_map.width + y) * (self.cell_size // 2) + self.offset_y
            pygame.draw.line(self.screen, (0, 100, 100), (start_x, start_y), (end_x, end_y))
    
    def draw_pixels(self):
        for pixel in self.pixel_map.pixels:
            x, y = pixel.position
            iso_x = (x - y) * self.cell_size + self.offset_x
            iso_y = (x + y) * (self.cell_size // 2) + self.offset_y + self.cell_size // 2
            points = [
                (iso_x, iso_y - self.cell_size // 2),
                (iso_x + self.cell_size, iso_y),
                (iso_x, iso_y + self.cell_size // 2),
                (iso_x - self.cell_size, iso_y)
            ]
            pygame.draw.polygon(self.screen, (255, 128, 0), points)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.pixel_map.pixels:
                    active_pixel = self.pixel_map.pixels[0]
                    if event.key == pygame.K_LEFT:
                        self.pixel_map.move_pixel_left(active_pixel)
                    elif event.key == pygame.K_RIGHT:
                        self.pixel_map.move_pixel_right(active_pixel)
                    elif event.key == pygame.K_UP:
                        self.pixel_map.move_pixel_up(active_pixel)
                    elif event.key == pygame.K_DOWN:
                        self.pixel_map.move_pixel_down(active_pixel)
                    
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_pixels()
            pygame.display.flip()
            
        pygame.quit()

if __name__ == "__main__":
    test_map = Map(20, 15)
    test_pixel = Pixel((5, 5))
    test_map.add_pixel(test_pixel)
    test_pixel_2 = Pixel((5, 6))
    test_map.add_pixel(test_pixel_2)
    
    test_map.move_pixel_right(test_pixel)
    
    display = PixelDisplay(test_map)
    display.run() 