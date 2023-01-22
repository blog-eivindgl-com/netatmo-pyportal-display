import displayio

class Humidity_Widget(displayio.Group):
    def __init__(self, cwd):
        super().__init__(x=0, y=0)
        self.humidity = 50
        self.battery_level = 100
        
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
        self.set_icon(self._day_sunny)
    
    def draw_widget(self, widget):
        self.humidity = int(widget['value'])
        self.battery_level = widget['batteryLevel']
        self.sunOrMoon = widget['sunOrMoon']
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
                self.set_icon(self._day_showers)
            else:
                self.set_icon(self._day_rain)
                # TODO: Look at temperature to see if it's snow instead of rain
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
                self.set_icon(self._night_showers)
            else:
                self.set_icon(self._night_rain)
                # TODO: Look at temperature to see if it's snow instead of rain

    def set_icon(self, filename):
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
