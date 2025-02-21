import tkinter as tk
from tkinter.font import Font
from pixel_map import Map, Pixel
import math

class PixelDisplay(tk.Tk):
    def __init__(self, pixel_map: Map, cell_size: int = 20):
        super().__init__()
        self.base_font_size = 5
        self.pixel_map = pixel_map
        self.cell_size = cell_size
        self.zoom = 1.0
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        
        self.title("Pixel Map")
        self.geometry(f"{800}x{600}")
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.bind_events()
        self.center_view()
        self.update_font()

    def bind_events(self):
        self.bind('<Key>', self.handle_key)
        self.bind('<Button-1>', self.start_drag)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.stop_drag)
        self.bind('<Button-4>', self.on_zoom_in)
        self.bind('<Button-5>', self.on_zoom_out)
        self.bind('<Configure>', self.on_resize)

    def center_view(self):
        self.offset_x = self.winfo_width() // 2
        self.offset_y = self.winfo_height() // 4

    def update_font(self):
        self.font = Font(family='Courier New', size=int(self.base_font_size * self.zoom))

    def grid_to_iso(self, x, y):
        return (
            (x - y) * self.cell_size * self.zoom + self.offset_x,
            (x + y) * (self.cell_size // 2) * self.zoom + self.offset_y
        )

    def draw_line(self, start, end):
        angle = math.atan2(end[1]-start[1], end[0]-start[0])
        mid = ((start[0]+end[0])/2, (start[1]+end[1])/2)
        text = '-----'
        text_width = self.font.measure(text)
        self.canvas.create_text(
            mid[0], mid[1],
            text=text,
            fill='#787878',
            font=self.font,
            angle=math.degrees(-angle)
        )

    def redraw(self):
        self.canvas.delete('all')
        self.draw_grid()
        self.draw_pixels()

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
            iso_x, iso_y = self.grid_to_iso(x, y)
            color = 'yellow' if i == 0 else 'orange'
            self.canvas.create_text(
                iso_x,
                iso_y + (self.cell_size * 2 * self.zoom * 0.25),
                text='*',
                fill=color,
                font=self.font
            )

    def handle_key(self, event):
        if event.keysym == 'space':
            self.center_view()
        elif self.pixel_map.pixels:
            self.handle_pixel_movement(event.keysym)
        self.redraw()

    def start_drag(self, event):
        self.dragging = True
        self.last_mouse_pos = (event.x, event.y)

    def stop_drag(self, event):
        self.dragging = False

    def on_drag(self, event):
        if self.dragging:
            dx = event.x - self.last_mouse_pos[0]
            dy = event.y - self.last_mouse_pos[1]
            self.offset_x += dx
            self.offset_y += dy
            self.last_mouse_pos = (event.x, event.y)
            self.redraw()

    def on_zoom_in(self, event):
        self.zoom *= 1.1
        self.update_font()
        self.redraw()

    def on_zoom_out(self, event):
        self.zoom *= 0.9
        self.update_font()
        self.redraw()

    def on_resize(self, event):
        self.center_view()
        self.redraw()

    def handle_pixel_movement(self, key):
        active_pixel = self.pixel_map.pixels[0]
        move_map = {
            'Left': self.pixel_map.move_pixel_left,
            'Right': self.pixel_map.move_pixel_right,
            'Up': self.pixel_map.move_pixel_up,
            'Down': self.pixel_map.move_pixel_down
        }
        if key in move_map:
            move_map[key](active_pixel) 

if __name__ == "__main__":
    pixel_map = Map(10, 10)
    pixel_map.add_pixel(Pixel(position=(0, 0)))
    pixel_map.add_pixel(Pixel(position=(4, 5)))
    pixel_map.add_pixel(Pixel(position=(9, 9)))
    pixel_display = PixelDisplay(pixel_map)
    pixel_display.mainloop()