import displayio
from adafruit_display_text.label import Label
from adafruit_datetime import datetime
import time

class Time_Widget(displayio.Group):
    def __init__(self, font, mode = "weekday"):
        super().__init__(x=0, y=240)
        WIDGET_WIDTH = 320
        WIDGET_HEIGHT = 80
        self.mode = mode

        self.time_text = Label(font, scale=2)
        self.time_text.color = 0xFFFFFF
        self.time_text.anchor_point = (0.0, 1.0)  # bottom left
        self.time_text.anchored_position = (0, WIDGET_HEIGHT)
        self.append(self.time_text)

        self.date_text = Label(font, scale=2)
        self.date_text.color = 0xFFFFFF
        self.date_text.anchor_point = (1.0, 1.0) # bottom right
        self.date_text.anchored_position = (WIDGET_WIDTH, WIDGET_HEIGHT)
        self.append(self.date_text)
    
    def draw_widget(self):
        self.update_time()
        self.update_date()

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

    def update_time(self):
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        second = now[5]
        if self.mode == "seconds":
            format_str = "%d:%02d:%02d"
            time_str = format_str % (hour, minute, second)
        else:
            format_str = "%d:%02d"
            time_str = format_str % (hour, minute)
        #print(time_str)
        self.time_text.text = time_str

    def update_date(self):
        now = time.localtime()
        day = now[2]
        month = now[1]
        if self.mode == "weekday":
            weekday = self.get_weekday(datetime.now().isoweekday())
            date_str = "%s %d/%d" % (weekday, day, month)
        else:
            date_str = "%d/%d" % (day, month)
        #print(date_str)
        self.date_text.text = date_str
    
    def change_mode(self):
        print("Time change mode")
        if self.mode == "weekday":
            self.mode = "seconds"
        else:
            self.mode = "weekday"
        self.update_time()
        self.update_date()