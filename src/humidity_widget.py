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

        self._weather_icon_sprite = None
        self._weather_icon_file = None
        self._weather_icon_group = displayio.Group(x=0, y=0)
        self.append(self._weather_icon_group)
        self.set_icon(self._day_sunny)
    
    def draw_widget(self, widget):
        self.humidity = int(widget['value'])
        self.battery_level = widget['batteryLevel']
        if self.humidity <= 10:
            self.set_icon(self._day_sunny)
        elif self.humidity <= 20:
            self.set_icon(self._day_sunny_overcast)
        elif self.humidity <= 30:
            self.set_icon(self._day_cloudy)
        elif self.humidity <= 40:
            self.set_icon(self._day_sprinkle)
        elif self.humidity <= 60:
            self.set_icon(self._day_showers)
        else:
            self.set_icon(self._day_rain)
            # TODO: Look at temperature to see if it's snow instead of rain
            # TODO: Look at time to see if it's night instead of day

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
