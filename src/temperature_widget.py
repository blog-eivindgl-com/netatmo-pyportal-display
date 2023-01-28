import displayio
from adafruit_display_text.label import Label

class Temperature_Widget(displayio.Group):
    def __init__(self, cwd, description_font, decimal_font, int_font):
        super().__init__(x=320, y=0)
        WIDGET_WIDTH = 160
        WIDGET_HEIGHT = 130
        self.mode = "current"
        self.temp = "0.0ºC"
        self.trend = "flat"
        self.min = "0.0ºC"
        self.min_time = "00.00 00:00"
        self.max = "0.0ºC"
        self.max_time = "00.00 00:00"
        
        self._flatIcon = cwd + "/icons/wi-trend-flat.bmp";
        self._upIcon = cwd + "/icons/wi-trend-up.bmp";
        self._downIcon = cwd + "/icons/wi-trend-down.bmp";
        self._minIcon = cwd + "/icons/wi-min.bmp";
        self._maxIcon = cwd + "/icons/wi-max.bmp";
        self._trend_icon_sprite = None
        self._trend_icon_file = None
        self._trend_icon_group = displayio.Group(x=80, y=40)
        self.append(self._trend_icon_group)
        self.set_icon(self._flatIcon)

        self.description = Label(description_font)
        self.append(self.description)
        self.description.anchor_point = (0.5, 1.0) # bottom middle
        self.description.anchored_position = (WIDGET_WIDTH / 2, WIDGET_HEIGHT)
        self.description.text = "temperature"

        self.tempInt = Label(int_font)
        self.append(self.tempInt)
        self.tempInt.color = 0xFFFFFF
        self.tempInt.anchor_point = (1.0, 1.0) # bottom right
        self.tempInt.anchored_position = (WIDGET_WIDTH / 2 - 10, WIDGET_HEIGHT - 35)

        self.tempDec = Label(decimal_font)
        self.append(self.tempDec)
        self.tempDec.color = 0xFFFFFF
        self.tempDec.anchor_point = (1.0, 0.0) # top right
        self.tempDec.anchored_position = (WIDGET_WIDTH, 0)
    
    def draw_widget(self, widget):
        if widget:
            self.temp = widget['value']
            self.trend = widget['trend']
            self.min = widget['minValue']
            self.min_time = widget['minTime']
            self.max = widget['maxValue']
            self.max_time = widget['maxTime']
            self.sensor = widget['description']

        if self.mode == "min":
            self.display_value(self.min)
            self.description.text = self.min_time
            self.set_icon(self._minIcon)
        elif self.mode == "max":
            self.display_value(self.max)
            self.description.text = self.max_time
            self.set_icon(self._maxIcon)
        else:
            self.display_value(self.temp)
            self.description.text = self.sensor

            if self.trend == "up":
                self.set_icon(self._upIcon)
            elif self.trend == "down":
                self.set_icon(self._downIcon)
            else:
                self.set_icon(self._flatIcon)

    def display_value(self, value):
        decPos = value.find(".")
        if decPos != -1:
            self.tempInt.text = value[:decPos]
            print("tempInt: ", self.tempInt.text)
            self.tempDec.text = value[decPos:]
            print("tempDec: ", self.tempDec.text)

    def set_icon(self, filename):
        print("Set trend icon to", filename)
        if (self._trend_icon_group):
            self._trend_icon_group.pop()
        
        if not filename:
            return
        
        if self._trend_icon_file:
            self._trend_icon_file.close()
        self._trend_icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._trend_icon_file)
        self._trend_icon_sprite = displayio.TileGrid(
            icon, pixel_shader=getattr(icon, 'pixel_shader', displayio.ColorConverter())
        )

        self._trend_icon_group.append(self._trend_icon_sprite)

    def change_mode(self):
        if self.mode == "current":
            self.mode = "min"
        elif self.mode == "min":
            self.mode = "max"
        else:
            self.mode = "current"
        print("%s widget change mode to %s" % (self.description.text, self.mode))
        self.draw_widget(None)