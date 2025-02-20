import pygame
from pixel_map import Map, Pixel
import math

class PixelDisplay:
    def __init__(self, pixel_map: Map, cell_size: int = 20):
        pygame.init()
        self.base_font_size = 14
        self.font = pygame.font.SysFont('Courier New', self.base_font_size)
        self.pixel_map = pixel_map
        self.cell_size = cell_size
        
        # Calculate window size based on map dimensions
        scale_factor = 1.5
        self.width = int((pixel_map.width + pixel_map.height) * cell_size * scale_factor)
        self.height = int((pixel_map.width + pixel_map.height) * cell_size * scale_factor * 0.9)
        
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Pixel Map")
        
        # Center the initial view
        self.center_view()
        
        self.zoom = 1.0
        self.dragging = False
        self.last_mouse_pos = None

    def center_view(self):
        self.offset_x = self.width // 2
        self.offset_y = self.height // 4

    def update_font(self):
        scaled_size = int(self.base_font_size * self.zoom)
        self.font = pygame.font.SysFont('Courier New', max(8, scaled_size))

    def grid_to_iso(self, x, y):
        return (
            (x - y) * self.cell_size * self.zoom + self.offset_x,
            (x + y) * (self.cell_size // 2) * self.zoom + self.offset_y
        )


    def draw_line(self, start, end):
        dx, dy = end[0] - start[0], end[1] - start[1]
        angle = math.degrees(math.atan2(dy, dx))
        
        line = self.font.render('---', True, (120, 120, 120))
        rotated = pygame.transform.rotate(line, -angle)
        self.screen.blit(rotated, rotated.get_rect(center=(
            (start[0] + end[0]) // 2,
            (start[1] + end[1]) // 2
        )))

    def draw_grid(self):
        for y in range(self.pixel_map.height + 1):
            for x in range(self.pixel_map.width):
                self.draw_line(
                    self.grid_to_iso(x, y),
                    self.grid_to_iso(x + 1, y)
                )

        for x in range(self.pixel_map.width + 1):
            for y in range(self.pixel_map.height):
                self.draw_line(
                    self.grid_to_iso(x, y),
                    self.grid_to_iso(x, y + 1)
                )

    def draw_pixels(self):
        for i, pixel in enumerate(self.pixel_map.pixels):
            x, y = pixel.position
            iso_pos = self.grid_to_iso(x, y)
            
            # Highlight active pixel
            color = (255, 255, 0) if i == 0 else (255, 128, 0)
            text = self.font.render('*', True, color)
            self.screen.blit(text, text.get_rect(center=(
                iso_pos[0],
                iso_pos[1] + (self.cell_size * 2 * self.zoom * 0.25)
            )))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.size
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.center_view()
                    elif self.pixel_map.pixels:
                        self.handle_pixel_movement(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.dragging = True
                        self.last_mouse_pos = event.pos
                    elif event.button == 4:  # Mouse wheel up
                        self.zoom *= 1.1
                        self.update_font()
                    elif event.button == 5:  # Mouse wheel down
                        self.zoom *= 0.9
                        self.update_font()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click release
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        current_pos = event.pos
                        dx = current_pos[0] - self.last_mouse_pos[0]
                        dy = current_pos[1] - self.last_mouse_pos[1]
                        self.offset_x += dx
                        self.offset_y += dy
                        self.last_mouse_pos = current_pos

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_pixels()
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS
            
        pygame.quit()

    def handle_pixel_movement(self, key):
        active_pixel = self.pixel_map.pixels[0]
        if key == pygame.K_LEFT:
            self.pixel_map.move_pixel_left(active_pixel)
        elif key == pygame.K_RIGHT:
            self.pixel_map.move_pixel_right(active_pixel)
        elif key == pygame.K_UP:
            self.pixel_map.move_pixel_up(active_pixel)
        elif key == pygame.K_DOWN:
            self.pixel_map.move_pixel_down(active_pixel)

if __name__ == "__main__":
    test_map = Map(20, 15)
    test_pixel = Pixel((5, 5))
    test_map.add_pixel(test_pixel)
    test_pixel_2 = Pixel((5, 6))
    test_map.add_pixel(test_pixel_2)
    
    test_map.move_pixel_right(test_pixel)
    
    display = PixelDisplay(test_map)
    display.run() 