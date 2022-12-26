import time
import json
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/" + __file__).rsplit('/', 1)[0]  # working directory

small_font = cwd + "/fonts/Arial-12.bdf"
medium_font = cwd + "/fonts/Arial-16.bdf"
large_font = cwd + "/fonts/Arial-Bold-24.bdf"

class Netatmo_Display(displayio.Group):
    def __init__(self, root_group):
        super().__init__

        root_group.append(self)
        self._icon_group = displayio.Group()
        self.append(self._icon_group)
        self._text_group = displayio.Group()
        self.append(self._text_group)

        self._icon_sprite = None
        self._icon_file = None
        self.set_icon(cwd + "/weather_background.bmp")

        self.small_font = bitmap_font.load_font(small_font)
        self.medium_font = bitmap_font.load_font(medium_font)
        self.large_font = bitmap_font.load_font(large_font)
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
        self.small_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(('°',))
        self.sensor_lable = None

        self.time_text = Label(self.medium_font)
        self.time_text.x = 200
        self.time_text.y = 12
        self.time_text.color = 0xFFFFFF
        self._text_group.append(self.time_text)

def draw_display(self):

    self.update_time()

def update_time(self):
    now = time.localtime()
    hour = now[3]
    minute = now[4]
    second = now[5]
    format_str = "%d:%02d:%02d"
    time_str = format_str % (hour, minute, second)
    print(time_str)
    self.time_text.text = time_str
