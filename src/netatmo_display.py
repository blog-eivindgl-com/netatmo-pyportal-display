import time
import json
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import temperature_widget  # pylint: disable=wrong-import-position
import humidity_widget  # pylint: disable=wrong-import-position
import time_widget  # pylint: disable=wrong-import-position

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

small_font = cwd+"/fonts/Arial-12.bdf"
time_font = cwd+"/fonts/Arial-16.bdf"
tempInt_font = cwd+"/fonts/BebasNeue-Regular-128.bdf"
tempDec_font = cwd+"/fonts/BebasNeue-Regular-64.bdf"

class Netatmo_Display(displayio.Group):
    def __init__(self, root_group):
        super().__init__()
        DISPLAY_WIDTH = 480
        DISPLAY_HEIGHT = 320
        TEMP_WIDGET_WIDTH = 160
        TEMP_WIDGET_HEIGHT = 160

        root_group.append(self)
        self._icon_group = displayio.Group(x=40)
        self.append(self._icon_group)
        self._text_group = displayio.Group()
        self.append(self._text_group)

        self.small_font = bitmap_font.load_font(small_font)
        self.time_font = bitmap_font.load_font(time_font)
        self.tempInt_font = bitmap_font.load_font(tempInt_font)
        self.tempDec_font = bitmap_font.load_font(tempDec_font)
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
        self.small_font.load_glyphs(glyphs)
        self.small_font.load_glyphs(('°',))
        self.time_font.load_glyphs(b'0123456789AEFHMORSTUW: ')
        self.tempInt_font.load_glyphs(glyphs)
        self.tempInt_font.load_glyphs(('°',))
        self.tempDec_font.load_glyphs(glyphs)
        self.tempDec_font.load_glyphs(('°',))

        self.humidity_widget = humidity_widget.Humidity_Widget(cwd)
        self._icon_group.append(self.humidity_widget)
        self.humidity_widget.x = 0
        self.humidity_widget.y = 0

        self.temp_widget_top = temperature_widget.Temperature_Widget(cwd, self.small_font, self.tempDec_font, self.tempInt_font)
        self._text_group.append(self.temp_widget_top)
        self.temp_widget_top.x = DISPLAY_WIDTH - TEMP_WIDGET_WIDTH
        self.temp_widget_top.y = 0

        self.temp_widget_bottom = temperature_widget.Temperature_Widget(cwd, self.small_font, self.tempDec_font, self.tempInt_font)
        self._text_group.append(self.temp_widget_bottom)
        self.temp_widget_bottom.x = DISPLAY_WIDTH - TEMP_WIDGET_WIDTH
        self.temp_widget_bottom.y = TEMP_WIDGET_HEIGHT + 30

        self.time_widget = time_widget.Time_Widget(self.time_font)
        self._text_group.append(self.time_widget)
        self.time_widget.x = 0
        self.time_widget.y = 240

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
            elif widget['type'] == "humidity":
                self.draw_humidity(widget)
        self.draw_time()

    def draw_temperature(self, widget):
        if widget['description'] == "Vestveggen ute":
            self.temp_widget_bottom.draw_widget(widget)
        elif widget['description'] == "Stua":
            self.temp_widget_top.draw_widget(widget)
    
    def draw_humidity(self, widget):
        self.humidity_widget.draw_widget(widget)

    def draw_time(self):
        self.time_widget.draw_widget()

    def draw_error(self):
        if self.error_text.text == "":
            now = time.localtime()
            hour = now[3]
            minute = now[4]
            second = now[5]
            self.error_text.text = "error at %d:%02d:%02d" % (hour, minute, second)

    def clear_error(self):
        self.error_text.text = ""
