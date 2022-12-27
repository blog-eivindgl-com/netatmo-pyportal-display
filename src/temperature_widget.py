import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import adafruit_imageload

class Temperature_Widget(displayio.TileGrid):
    def __init__(self, netatmo_display_group, small_font, meduim_font, large_font):
        sprite_sheet, palette = adafruit_imageload.load("/weather_background.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
        super().__init__(bitmap=sprite_sheet, pixel_shader=palette)
        netatmo_display_group.append(self)
        self.width = 3
        self.height = 2
        self.tile_width = 10
        self.tile_height = 10

        self.minus = Label(meduim_font)
        self.minus.color = 0xFFFFFF
        self.minus.text = "-"
        self[0, 1] = self.minus

        self.temp = Label(large_font)
        self.temp.color = 0xFFFFFF
        self.temp.text = ""
        self[1, 1] = self.temp
    
    def draw_widget(self, widget):
        self.temp.text = widget['value']

