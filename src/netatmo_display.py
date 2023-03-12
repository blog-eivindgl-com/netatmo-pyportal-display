import time
import json
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
import temperature_widget  # pylint: disable=wrong-import-position
import humidity_widget  # pylint: disable=wrong-import-position
import time_widget  # pylint: disable=wrong-import-position
import wind_widget # pylint: disable=wrong-import-positiion

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

small_font = cwd+"/fonts/Arial-12.bdf"
time_font = cwd+"/fonts/Arial-16.bdf"
tempInt_font = cwd+"/fonts/BebasNeue-Regular-128.bdf"
tempDec_font = cwd+"/fonts/BebasNeue-Regular-64.bdf"
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
TEMP_WIDGET_WIDTH = 160
TEMP_WIDGET_HEIGHT = 160

class Netatmo_Display(displayio.Group):
    def __init__(self, root_group):
        super().__init__()

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
        self.tempInt_font.load_glyphs(b'0123456789CM-.: ')
        self.tempInt_font.load_glyphs(('°',))
        self.tempDec_font.load_glyphs(b'0123456789CM-.: ')
        self.tempDec_font.load_glyphs(('°',))

        self.humidity_widget = humidity_widget.Humidity_Widget(cwd, self.small_font)
        self._icon_group.append(self.humidity_widget)
        self.humidity_widget.x = 40 
        self.humidity_widget.y = 0

        self.strength = float(0)
        self.angle = float(0)
        self.wind_widget = wind_widget.Wind_Widget(self.small_font)
        self._icon_group.append(self.wind_widget)
        self.wind_widget.x = 0
        self.wind_widget.y = 190

        self.wind_widget_gusts = wind_widget.Wind_Widget(self.small_font)
        self._icon_group.append(self.wind_widget_gusts)
        self.wind_widget_gusts.x = 160
        self.wind_widget_gusts.y = 190

        self.temp_widget_top = temperature_widget.Temperature_Widget(cwd, self.small_font, self.tempDec_font, self.tempInt_font)
        self._text_group.append(self.temp_widget_top)
        self.temp_widget_top.x = DISPLAY_WIDTH - TEMP_WIDGET_WIDTH
        self.temp_widget_top.y = 0
        self.temp_widget_top.default_module = "Stua"

        self.temp_widget_bottom = temperature_widget.Temperature_Widget(cwd, self.small_font, self.tempDec_font, self.tempInt_font)
        self._text_group.append(self.temp_widget_bottom)
        self.temp_widget_bottom.x = DISPLAY_WIDTH - TEMP_WIDGET_WIDTH
        self.temp_widget_bottom.y = TEMP_WIDGET_HEIGHT + 30

        self.time_widget = time_widget.Time_Widget(self.time_font, mode="weekday")
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
        if weather:
            weather = json.loads(weather)
            for widget in weather['widgets']:
                if widget['type'] == "temperature":
                    self.draw_temperature(widget)
                elif widget['type'] == "humidity":
                    self.draw_humidity(widget)
                elif widget['type'] == "wind":
                    self.draw_wind(widget)

    def animate_wind(self):
        # TODO: remove this fake wind widget
        self.strength = float(self.strength) + 0.2
        self.angle = float(self.angle) + 0.2
        if self.strength >= 34:
            self.strength = float(0)
        if self.angle >= 360:
            self.angle = float(0)
        wind = json.loads('{ "type": "wind", "value": "%fm/s", "angle": %f, "batteryLevel": 88, "description": "Vind" }' % (self.strength, self.angle))
        self.draw_wind(wind)
        wind = json.loads('{ "type": "wind", "value": "%fm/s", "angle": %f, "batteryLevel": 88, "description": "Kast" }' % (self.strength, self.angle))
        self.draw_wind(wind)

    def draw_temperature(self, widget):
        if widget['description'] == "Vestveggen ute" or widget['description'] == "Østveggen ute":
            self.temp_widget_bottom.draw_widget(widget)
        elif widget['description'] == "Stua" or widget['description'] == "Boden":
            self.temp_widget_top.draw_widget(widget)
    
    def draw_humidity(self, widget):
        self.humidity_widget.draw_widget(widget)

    def draw_wind(self, widget):
        if (widget['description'] == "Kast"):
            self.wind_widget_gusts.draw_widget(widget)
        else:
            self.wind_widget.draw_widget(widget)

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

    def touch(self, touch_point):
        print(touch_point)
        x, y, pressure = touch_point
        if self.temp_widget_top.x <= x and self.temp_widget_bottom.y >= y:
            self.temp_widget_top.change_mode()
        elif self.temp_widget_bottom.x <= x and self.temp_widget_bottom.y <= y:
            self.temp_widget_bottom.change_mode()
        elif self.time_widget.x <= x and self.temp_widget_bottom.x > x and self.time_widget.y <= y:
            self.time_widget.change_mode()
        elif self.wind_widget.x <= x and self.wind_widget.x + 160 >= x and self.wind_widget.y <= y and self.wind_widget.y + 80 >= y:
            self.wind_widget.change_mode()
        elif self.wind_widget_gusts.x <= x and self.temp_widget_bottom.x > x and self.wind_widget_gusts.y <= y and self.wind_widget_gusts.y + 80 >= y:
            self.wind_widget_gusts.change_mode()
        else:
            self.humidity_widget.change_mode()
