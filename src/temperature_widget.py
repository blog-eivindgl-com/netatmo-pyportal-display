import displayio
from adafruit_datetime import datetime
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
        self.modules = []
        self.selected_module = None
        self.selected_module_at = None
        self.has_cycled_through_module = False
        self.default_module = None
        
        self._flatIcon = cwd + "/icons/wi-trend-flat.bmp"
        self._upIcon = cwd + "/icons/wi-trend-up.bmp"
        self._downIcon = cwd + "/icons/wi-trend-down.bmp"
        self._minIcon = cwd + "/icons/wi-min.bmp"
        self._maxIcon = cwd + "/icons/wi-max.bmp"
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
            self.update_module_data(widget)

        if self.selected_module == None and self.default_module != None:
            print("Setting default module %s" % self.default_module)
            self.selected_module = self.find_default_module()
            if self.selected_module == None:
                self.display_module(self.modules[0][1]) # couldn't find the default module, so display the first one
            else:
                print("Default module was found at index %s" % self.selected_module)
                self.display_module(self.modules[self.selected_module][1])
        elif self.default_module == None and (self.selected_module_at == None or (datetime.now() - self.selected_module_at).total_seconds() > 360):
            self.display_module(self.find_module_with_lowest_temperature())
        else:
            self.display_module(self.modules[self.selected_module][1])

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

    def find_default_module(self):
        for i in range(len(self.modules)):
            if self.modules[i][1]['description'] == self.default_module:
                return i
        return None

    def update_module_data(self, widget):
        isReplaced = False
        for i in range(len(self.modules)):
            if self.modules[i][1]['description'] == widget['description']:
                self.modules[i] = (widget['description'], widget)
                isReplaced = True
        if not isReplaced:
            self.modules.append((widget['description'], widget))            

    def find_module_with_lowest_temperature(self):
        lowTempModule = None
        print('modules length: %s' % len(self.modules))
        for t in self.modules:
            if lowTempModule == None:
                lowTempModule = t[1]
            else:
                thisTemp = self.temp_as_decimal(t[1]['value'])
                print('This temp: %s was parsed to %s' % (t[1]['value'], thisTemp))
                lowTemp = self.temp_as_decimal(lowTempModule['value'])
                print('low temp: %s was parsed to %s' % (lowTempModule['value'], lowTemp))
                if thisTemp < lowTemp:
                    lowTempModule = t[1]
        print('lowTempModule: %s' % lowTempModule)
        return lowTempModule

    def display_module(self, module):
        if module:
            self.temp = module['value']
            self.trend = module['trend']
            self.min = module['minValue']
            self.min_time = module['minTime']
            self.max = module['maxValue']
            self.max_time = module['maxTime']
            self.sensor = module['description']

    def temp_as_decimal(self, tempStr):
        tempInt = 0
        tempDec = 0
        decPos = tempStr.find(".")
        if decPos != -1:
            tempInt = tempStr[:decPos]
            tempDec = tempStr[decPos+1:decPos+2]
        return float(f'{tempInt}.{tempDec}')

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
        # if more than one module is used by this widget, 
        # cycle through them and make sure not the one with
        # lowest temperature is the one automatically displayed for a while
        if self.has_cycled_through_module and len(self.modules) > 1:
            if self.selected_module == None:
                self.selected_module = 0
            else:
                self.selected_module = self.selected_module + 1
                if self.selected_module >= len(self.modules):
                    self.selected_module = 0
            print("Changed module to %s" % self.modules[self.selected_module][1]['description'])
            self.selected_module_at = datetime.now()
            self.draw_widget(None)
            self.has_cycled_through_module = False
            return

        if self.mode == "current":
            self.mode = "min"
        elif self.mode == "min":
            self.mode = "max"
        else:
            self.mode = "current"
            self.has_cycled_through_module = True
        print("%s widget change mode to %s" % (self.description.text, self.mode))
        self.draw_widget(None)