import displayio
import math
import gc
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text.label import Label

WIND_WIDGET_WIDTH = 80
WIND_WIDGET_HEIGHT = 80

class Wind_Widget(displayio.Group):
    def __init__(self, description_font):
        super().__init__(x=0, y=0)
        self.strength = float(50)
        self.angle = float(2)
        self.battery_level = 100
        self.origin_x = WIND_WIDGET_WIDTH / 2
        self.origin_y = WIND_WIDGET_HEIGHT / 2
        self.arrow_length = WIND_WIDGET_WIDTH / 2
        self.arrow_width = float(14)
        self.arrow_stretch = float(7)
        self.gap = float(5)
        self.indicator_length = self.arrow_length / 3
        self.small_indicator_length = self.indicator_length * 2 / 3
        
        self._wind_arrow_group = displayio.Group(x=0, y=0, scale=1)
        self.append(self._wind_arrow_group)
        self.description = Label(description_font)
        self.append(self.description)
        self.description.anchor_point = (0.5, 1.0) # bottom middle
        self.description.anchored_position = (WIND_WIDGET_WIDTH / 2, WIND_WIDGET_HEIGHT + 20)
        self.description.text = "wind"
    
    def draw_widget(self, widget):
        value = widget['value']
        mPos = value.find("m")
        if mPos != -1:
            self.strength = float(value[:mPos])
            print("wind strength: ", self.strength)

        self.angle = float(widget['angle'])
        print("wind angle: ", self.angle)
        self.battery_level = widget['batteryLevel']
        self.arrow_x = self.origin_x + self.arrow_length * math.cos(self.angle)
        self.arrow_y = self.origin_y + self.arrow_length * math.sin(self.angle)
        self.description.text = "%.1fm/s" % self.strength
        self.remove(self._wind_arrow_group)
        gc.collect()
        self._wind_arrow_group = displayio.Group(x=0, y=0, scale=1)
        self.append(self._wind_arrow_group)

        #if self.strength <= .2:
            # Stille
        if self.strength > .2 and self.strength <= 1.5:
            # Flau vind
            self.draw_arrow()
        elif self.strength <= 3.3:
            # Svak vind (short indicator)
            self.draw_arrow()
            self.draw_strength_indicator(0, "short")
        elif self.strength <= 5.4:
            # Lett bris (long indicator)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
        elif self.strength <= 7.9:
            # Laber bris (short and long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "short")
        elif self.strength <= 10.7:
            # Frisk bris (two long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "long")
        elif self.strength <= 13.8:
            # Liten kuling (short and two long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "long")
            self.draw_strength_indicator(2, "short")
        elif self.strength <= 17.1:
            # Stiv kuling (three long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "long")
            self.draw_strength_indicator(2, "long")
        elif self.strength <= 20.7:
            # Sterk kuling (short and three long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "long")
            self.draw_strength_indicator(2, "long")
            self.draw_strength_indicator(3, "short")
        elif self.strength <= 24.4:
            # Liten storm (short and four long indicators)
            self.draw_arrow()
            self.draw_strength_indicator(0, "long")
            self.draw_strength_indicator(1, "long")
            self.draw_strength_indicator(2, "long")
            self.draw_strength_indicator(3, "long")
            self.draw_strength_indicator(4, "short")
        elif self.strength <= 28.4:
            # Full storm (flag indicator)
            self.draw_arrow()
            self.draw_flag()
        elif self.strength <= 32.6:
            # Sterk storm (flag and long indicator)
            self.draw_arrow()
            self.draw_flag()
            self.draw_strength_indicator(2, "long")
        else:
            # Orkan (flag and two long indicators)
            self.draw_arrow()
            self.draw_flag()
            self.draw_strength_indicator(2, "long")
            self.draw_strength_indicator(3, "long")

    def draw_arrow(self):
        # Draw line
        r = Line(int(self.origin_x), int(self.origin_y), int(self.arrow_x), int(self.arrow_y), color=0xFFFFFF)

        # Draw arrow head
        points = []
        points.append((int(self.arrow_x), int(self.arrow_y)))
        points.append(
            (
            int(self.arrow_x - self.arrow_width * math.cos(self.angle + math.pi / self.arrow_stretch)), 
            int(self.arrow_y - self.arrow_width * math.sin(self.angle + math.pi / self.arrow_stretch))
            ))
        points.append(
            (
            int(self.arrow_x - self.arrow_width * math.cos(self.angle - math.pi / self.arrow_stretch)), 
            int(self.arrow_y - self.arrow_width * math.sin(self.angle - math.pi / self.arrow_stretch))
            ))
        ah = Triangle(points[0][0], points[0][1], points[1][0], points[1][1], points[2][0], points[2][1], fill=0xFFFFFF, outline=0xFFFFFF)

        self._wind_arrow_group.append(r)
        self._wind_arrow_group.append(ah)

    def draw_strength_indicator(self, indicator_no, indicator_type):
        len = self.indicator_length
        if indicator_type == "short":
            len = self.small_indicator_length
        start_x = self.origin_x + self.gap * float(indicator_no) * math.cos(self.angle)
        start_y = self.origin_y + self.gap * float(indicator_no) * math.sin(self.angle)
        end_x = start_x + len * math.sin(self.angle)
        end_y = start_y - len * math.cos(self.angle)
        indicator = Line(int(start_x), int(start_y), int(end_x), int(end_y), 0xFFFFFF)
        self._wind_arrow_group.append(indicator)
    
    def draw_flag(self):
        end_x = self.origin_x + self.gap * math.cos(self.angle)
        end_y = self.origin_y + self.gap * math.sin(self.angle)
        middle_x = self.origin_x + (self.gap / 2 - 1) * math.cos(self.angle)
        middle_y = self.origin_y + (self.gap / 2 - 1) * math.sin(self.angle)
        tip_x = middle_x + self.indicator_length * math.sin(self.angle)
        tip_y = middle_y - self.indicator_length * math.cos(self.angle)
        flag = Triangle(int(self.origin_x), int(self.origin_y), int(tip_x), int(tip_y), int(end_x), int(end_y), fill=0xFFFFFF, outline=0xFFFFFF)
        self._wind_arrow_group.append(flag)