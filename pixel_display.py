import pygame
from pixel_map import Map, Pixel

class PixelDisplay:
    def __init__(self, pixel_map: Map, cell_size: int = 20):
        pygame.init()
        self.pixel_map = pixel_map
        self.cell_size = cell_size
        self.width = pixel_map.width * cell_size
        self.height = pixel_map.height * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pixel Map")
        
    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (0, 100, 100), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (0, 100, 100), (0, y), (self.width, y))
    
    def draw_pixels(self):
        for pixel in self.pixel_map.pixels:
            x, y = pixel.position
            rect = pygame.Rect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, (255, 128, 0), rect)
    
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