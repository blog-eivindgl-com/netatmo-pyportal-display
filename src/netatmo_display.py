import time
from adafruit_datetime import datetime
import json
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import temperature_widget  # pylint: disable=wrong-import-position

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

small_font = cwd+"/fonts/Arial-12.bdf"
medium_font = cwd+"/fonts/Arial-16.bdf"
large_font = cwd+"/fonts/Arial-Bold-24.bdf"

class Netatmo_Display(displayio.Group):
    def __init__(self, root_group):
        super().__init__()

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

        self.outdoor_temp = Label(self.medium_font, scale=3)
        self.outdoor_temp.x = 100
        self.outdoor_temp.y = 50
        self.outdoor_temp.color = 0xFFFFFF
        self._text_group.append(self.outdoor_temp)

        self.indoor_temp = Label(self.medium_font, scale=3)
        self.indoor_temp.x = 100
        self.indoor_temp.y = 100
        self.indoor_temp.color = 0xFFFFFF
        self._text_group.append(self.indoor_temp)

        self.time_text = Label(self.medium_font, scale=2)
        self.time_text.x = 300
        self.time_text.y = 300
        self.time_text.color = 0xFFFFFF
        self._text_group.append(self.time_text)

        self.error_text = Label(self.small_font)
        self.error_text.x = 10
        self.error_text.y = 10
        self.error_text.color = 0xFF0000
        self.error_text.text = ""
        self._text_group.append(self.error_text)

    def draw_display(self, weather):
        weather = json.loads(weather)
        for widget in weather['widgets']:
            if widget['type'] == "temperature":
                self.draw_temperature(widget)
        self.update_time()

    def draw_temperature(self, widget):
        if widget['description'] == "Vestveggen ute":
            self.outdoor_temp.text = widget['value']
        elif widget['description'] == "Stua":
            self.indoor_temp.text = widget['value']
    
    def draw_error(self):
        if self.error_text.text == "":
            now = time.localtime()
            hour = now[3]
            minute = now[4]
            second = now[5]
            self.error_text.text = "error at %d:%02d:%02d" % (hour, minute, second)

    def clear_error(self):
        self.error_text.text = ""

    def get_weekday(self, isoweekday):
        if isoweekday == 1:
            return "MO"
        elif isoweekday == 2:
            return "TU"
        elif isoweekday == 3:
            return "WE"
        elif isoweekday == 4:
            return "TH"
        elif isoweekday == 5:
            return "FR"
        elif isoweekday == 6:
            return "SA"
        return "SU" 

    def update_time(self, mode = "weekday"):
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        second = now[5]
        weekday = self.get_weekday(datetime.now().isoweekday())
        if mode == "seconds":
            format_str = "%d:%02d:%02d"
            time_str = format_str % (hour, minute, second)
        else:
            format_str = "%d:%02d %s"
            time_str = format_str % (hour, minute, weekday)
        print(time_str)
        self.time_text.text = time_str

    def set_icon(self, filename):
        print("Set icon to", filename)
        if (self._icon_group):
            self._icon_group.pop()
        
        if not filename:
            return
        
        if self._icon_file:
            self._icon_file.close()
        self._icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._icon_file)
        self._icon_sprite = displayio.TileGrid(
            icon, pixel_shader=getattr(icon, 'pixel_shader', displayio.ColorConverter())
        )

        self._icon_group.append(self._icon_sprite)