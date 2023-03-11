import displayio
import gc
import gui_object
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect

class Humidity_Widget(displayio.Group):
    def __init__(self, cwd, description_font):
        super().__init__(x=0, y=0)
        self.humidity = 50
        self.mode = "humidity"
        
        # day weather
        self._day_sunny = cwd + "/icons/wi-day-sunny.bmp";
        self._day_sunny_overcast = cwd + "/icons/wi-day-sunny-overcast.bmp";
        self._day_cloudy = cwd + "/icons/wi-day-cloudy.bmp";
        self._day_sprinkle = cwd + "/icons/wi-day-sprinkle.bmp";
        self._day_showers = cwd + "/icons/wi-day-showers.bmp";
        self._day_rain = cwd + "/icons/wi-day-rain.bmp";
        self._day_sleet = cwd + "/icons/wi-day-sleet.bmp";
        self._day_snow = cwd + "/icons/wi-day-snow.bmp";

        # night weather
        self._night_clear = cwd + "/icons/wi-night-clear.bmp";
        self._night_partly_cloudy = cwd + "/icons/wi-night-partly-cloudy.bmp";
        self._night_cloudy = cwd + "/icons/wi-night-cloudy.bmp";
        self._night_sprinkle = cwd + "/icons/wi-night-sprinkle.bmp";
        self._night_showers = cwd + "/icons/wi-night-showers.bmp";
        self._night_rain = cwd + "/icons/wi-night-rain.bmp";
        self._night_sleet = cwd + "/icons/wi-night-sleet.bmp";
        self._night_snow = cwd + "/icons/wi-night-snow.bmp";

        self._weather_icon_sprite = None
        self._weather_icon_file = None
        self._weather_icon_group = displayio.Group(x=0, y=0, scale=1)
        self.append(self._weather_icon_group)        

        # battery indicators
        self._battery_indicators_group = displayio.Group(x=-30, y=10, scale=1)
        self.append(self._battery_indicators_group)
        self._battery_indicator_label = Label(description_font)
        self.append(self._battery_indicator_label)
        self._battery_indicator_label.anchor_point = (0.0, 0.0) # upper left
        self._battery_indicator_label.anchored_position = (0, 10)
        self._battery_indicator_label.text = ""

        # update icon after everything is setup
        self.set_icon(self._day_sunny)
    
    def draw_widget(self, widget):
        if widget:
            self.humidity = int(widget['value'])
            self.battery_indicators = widget['batteryIndicators']
            self.sunOrMoon = widget['sunOrMoon']
            self.outTemp = widget['outTemp']
        
        # clear the area where battery indicators are drawn and add a new empty group
        self.remove(self._battery_indicators_group)
        self._battery_indicators_group = None
        gc.collect()
        self._battery_indicators_group = displayio.Group(x=-30, y=0, scale=1)
        self.append(self._battery_indicators_group)

        # if any battery indicator is less than 10%, 
        # switch between displaying humidity and battery indicators to warn the user
        low_battery = False
        for bi in self.battery_indicators:
            if bi['batteryLevel'] < 10:
                low_battery = True
        
        if low_battery:
            if self.mode == "humidity":
                self.mode = "battery_indicators"
            else:
                self.mode = "humidity"

        if self.mode == "humidity":
            self.draw_humidity()
        elif self.mode == "battery_indicators":
            self.draw_battery_indicators()

    def draw_humidity(self):
        if (self.sunOrMoon == 'sun'):
            if self.humidity <= 60:
                self.set_icon(self._day_sunny)
            elif self.humidity <= 65:
                self.set_icon(self._day_sunny_overcast)
            elif self.humidity <= 70:
                self.set_icon(self._day_cloudy)
            elif self.humidity <= 80:
                self.set_icon(self._day_sprinkle)
            elif self.humidity <= 85:
                if self.outTemp > 1:
                    self.set_icon(self._day_showers)
                else:
                    self.set_icon(self._day_sleet)
            else:
                if self.outTemp > 0:
                    self.set_icon(self._day_rain)
                else:
                    self.set_icon(self._day_snow)
        else:
            if self.humidity <= 60:
                self.set_icon(self._night_clear)
            elif self.humidity <= 65:
                self.set_icon(self._night_partly_cloudy)
            elif self.humidity <= 70:
                self.set_icon(self._night_cloudy)
            elif self.humidity <= 80:
                self.set_icon(self._night_sprinkle)
            elif self.humidity <= 85:
                if self.outTemp > 1:
                    self.set_icon(self._night_showers)
                else:
                    self.set_icon(self._night_sleet)
            else:
                if self.outTemp > 0:
                    self.set_icon(self._night_rain)
                else:
                    self.set_icon(self._night_snow)
    
    def draw_battery_indicators(self):
        module_names = ""
        self.set_icon(None)
        gc.collect()
        indicatorNo = 0
        for bi in self.battery_indicators:
            module_names += bi['moduleName'] + "\n"
            self._battery_indicators_group.append(
                # border of indicator
                Rect(x=0, y=(indicatorNo * 28 + 11), width=25, height=10, fill=None, outline=0xFFFFFF, stroke=1)
            )
            fill = 0x00AA00
            if bi['batteryLevel'] < 10:
                fill = 0xAA0000
            elif bi['batteryLevel'] < 30:
                fill = 0xAAAA00
            self._battery_indicators_group.append(
                # fill of indicator
                Rect(x=1, y=(indicatorNo * 28 + 12), width=int(23 * bi['batteryLevel'] / 100), height=8, fill=fill, outline=fill, stroke=1)
            )
            indicatorNo = indicatorNo + 1
        self._battery_indicator_label.text = module_names
        gc.collect()

    def set_icon(self, filename):
        if self._battery_indicator_label:
            self._battery_indicator_label.text = ""
        print("Set weather icon to", filename)

        if (self._weather_icon_group):
            self._weather_icon_group.pop()
        
        if not filename:
            return
        
        if self._weather_icon_file:
            self._weather_icon_file.close()
        self._weather_icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._weather_icon_file)
        self._weather_icon_sprite = displayio.TileGrid(
            icon, pixel_shader=getattr(icon, 'pixel_shader', displayio.ColorConverter())
        )

        self._weather_icon_group.append(self._weather_icon_sprite)
        gc.collect()

    def change_mode(self):
        if self.mode == "humidity":
            self.mode = "battery_indicators"
        else:
            self.mode = "humidity"
        self.draw_widget(None)
        print("Humidity change mode")
