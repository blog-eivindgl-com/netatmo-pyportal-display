import displayio
import math
import gc
import gui_object
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text.label import Label

WIND_WIDGET_WIDTH = 80
WIND_WIDGET_HEIGHT = 80
FONT_SIZE = 12

class Wind_Widget(displayio.Group):
    def __init__(self, description_font):
        super().__init__(x=0, y=0)
        self.strength = float(50)
        self.angle = float(2)
        self.battery_level = 100
        self.origin_x = WIND_WIDGET_WIDTH / 2
        self.origin_y = WIND_WIDGET_HEIGHT / 2
        self.arrow_length = float(min(WIND_WIDGET_HEIGHT - FONT_SIZE - 2, WIND_WIDGET_WIDTH))
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
        self.description.anchored_position = (WIND_WIDGET_WIDTH / 2, WIND_WIDGET_HEIGHT)
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
        self.description.text = "%s %.1fm/s" % (widget['description'], self.strength)
        self.remove(self._wind_arrow_group)
        gc.collect()
        self._wind_arrow_group = displayio.Group(x=0, y=0, scale=1)
        self.append(self._wind_arrow_group)
        gui_objects = self.create_gui_objects()
        self.center_objects(gui_objects)
        gc.collect()
        self.draw_gui_objects(gui_objects)
        gui_objects = None
        gc.collect()
        
    def center_objects(self, gui_objects):
        if len(gui_objects) == 0:
            return
        
        min_x = float(1000)
        min_y = float(1000)
        max_x = float(-1000)
        max_y = float(-1000)

        # find width and height of all objects
        for obj in gui_objects:
            if obj.min_x < min_x:
                min_x = obj.min_x
            if obj.min_y < min_y:
                min_y = obj.min_y
            if obj.max_x > max_x:
                max_x = obj.max_x
            if obj.max_y > max_y:
                max_y = obj.max_y
        
        total_w = max_x - min_x
        total_h = max_y - min_y
        ideal_x = float(WIND_WIDGET_WIDTH) / float(2) - total_w / float(2)
        ideal_y = float(WIND_WIDGET_HEIGHT) / float(2) - total_h / float(2) - self.description.height
        shift_x = ideal_x - min_x
        shift_y = ideal_y - min_y

        # reposition all points
        for obj in gui_objects:
            points = []
            for p in obj.points:
                points.append((p[0] + shift_x, p[1] + shift_y))
            obj.points = points
                

    def draw_gui_objects(self, gui_objects):
        for obj in gui_objects:
            if obj.type == "line":
                l = Line(int(obj.points[0][0]), int(obj.points[0][1]), int(obj.points[1][0]), int(obj.points[1][1]), color=0xFFFFFF)
                self._wind_arrow_group.append(l)
            elif obj.type == "triangle":
                t = Triangle(int(obj.points[0][0]), int(obj.points[0][1]), int(obj.points[1][0]), int(obj.points[1][1]), int(obj.points[2][0]), int(obj.points[2][1]), outline=0xFFFFFF, fill=0xFFFFFF)
                self._wind_arrow_group.append(t)

    def create_gui_objects(self):
        gui_objects = []

        #if self.strength <= .2:
            # Stille
        if self.strength > .2 and self.strength <= 1.5:
            # Flau vind
            self.create_arrow(gui_objects)
        elif self.strength <= 3.3:
            # Svak vind (short indicator)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "short", gui_objects)
        elif self.strength <= 5.4:
            # Lett bris (long indicator)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
        elif self.strength <= 7.9:
            # Laber bris (short and long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "short", gui_objects)
        elif self.strength <= 10.7:
            # Frisk bris (two long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "long", gui_objects)
        elif self.strength <= 13.8:
            # Liten kuling (short and two long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "long", gui_objects)
            self.create_strength_indicator(2, "short", gui_objects)
        elif self.strength <= 17.1:
            # Stiv kuling (three long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "long", gui_objects)
            self.create_strength_indicator(2, "long", gui_objects)
        elif self.strength <= 20.7:
            # Sterk kuling (short and three long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "long", gui_objects)
            self.create_strength_indicator(2, "long", gui_objects)
            self.create_strength_indicator(3, "short", gui_objects)
        elif self.strength <= 24.4:
            # Liten storm (short and four long indicators)
            self.create_arrow(gui_objects)
            self.create_strength_indicator(0, "long", gui_objects)
            self.create_strength_indicator(1, "long", gui_objects)
            self.create_strength_indicator(2, "long", gui_objects)
            self.create_strength_indicator(3, "long", gui_objects)
            self.create_strength_indicator(4, "short", gui_objects)
        elif self.strength <= 28.4:
            # Full storm (flag indicator)
            self.create_arrow(gui_objects)
            self.create_flag(gui_objects)
        elif self.strength <= 32.6:
            # Sterk storm (flag and long indicator)
            self.create_arrow(gui_objects)
            self.create_flag(gui_objects)
            self.create_strength_indicator(2, "long", gui_objects)
        else:
            # Orkan (flag and two long indicators)
            self.create_arrow(gui_objects)
            self.create_flag(gui_objects)
            self.create_strength_indicator(2, "long", gui_objects)
            self.create_strength_indicator(3, "long", gui_objects)
        
        return gui_objects

    def create_arrow(self, gui_objects):
        # Draw line
        r = gui_object.Gui_Object("line", [(self.origin_x, self.origin_y), (self.arrow_x, self.arrow_y)])

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
        ah = gui_object.Gui_Object("triangle", [(points[0][0], points[0][1]), (points[1][0], points[1][1]), (points[2][0], points[2][1])])

        gui_objects.append(r)
        gui_objects.append(ah)

    def create_strength_indicator(self, indicator_no, indicator_type, gui_objects):
        len = self.indicator_length
        if indicator_type == "short":
            len = self.small_indicator_length
        start_x = self.origin_x + self.gap * float(indicator_no) * math.cos(self.angle)
        start_y = self.origin_y + self.gap * float(indicator_no) * math.sin(self.angle)
        end_x = start_x + len * math.sin(self.angle)
        end_y = start_y - len * math.cos(self.angle)
        indicator = gui_object.Gui_Object("line", [(start_x, start_y), (end_x, end_y)])
        gui_objects.append(indicator)
    
    def create_flag(self, gui_objects):
        end_x = self.origin_x + self.gap * math.cos(self.angle)
        end_y = self.origin_y + self.gap * math.sin(self.angle)
        middle_x = self.origin_x + (self.gap / 2 - 1) * math.cos(self.angle)
        middle_y = self.origin_y + (self.gap / 2 - 1) * math.sin(self.angle)
        tip_x = middle_x + self.indicator_length * math.sin(self.angle)
        tip_y = middle_y - self.indicator_length * math.cos(self.angle)
        flag = gui_object.Gui_Object("triangle", [(self.origin_x, self.origin_y), (tip_x, tip_y), (end_x, end_y)])
        gui_objects.append(flag)