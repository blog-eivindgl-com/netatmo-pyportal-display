import sys
import board
import time
import gc
from adafruit_pyportal import PyPortal
import adafruit_touchscreen
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
import netatmo_display  # pylint: disable=wrong-import-position

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set up where we'll be fetching data from
DATA_SOURCE = "http://192.168.1.104:8082/api/display"
DATA_LOCATION = []

# Prepare sounds
beep_sound = cwd+"/sounds/beep.wav"

# Initialize the pyportal object and let us know what data to fetch and where
# to display it
initial_mem = gc.mem_free()
pyportal = PyPortal(
                    url=DATA_SOURCE,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)
touch = adafruit_touchscreen.Touchscreen(
                    board.TOUCH_XL, 
                    board.TOUCH_XR, 
                    board.TOUCH_YD, 
                    board.TOUCH_YU,
                    calibration=((5200, 59000), (5800, 57000)),
                    size=(480, 320))
gc.collect()
pyportal_mem = gc.mem_free()
gfx = netatmo_display.Netatmo_Display(pyportal.splash)
gc.collect()
netatmo_mem = gc.mem_free()
print("Pyportal takes {}B of memory".format(initial_mem - pyportal_mem))
print("NetatmoDisplay takes {}B of memory".format(pyportal_mem - netatmo_mem))
localtile_refresh = None
weather_refresh = None
loop_refresh = None
reload_count = 0
updateTime = .5
while True:
    # reach to touch but don't update everything on every loop
    if (not loop_refresh) or (time.monotonic() - loop_refresh) > updateTime:
        loop_refresh = time.monotonic()
        gc.collect()
        start_mem = gc.mem_free()
        print("Free mem before updates: {}B".format(start_mem))

    # only query the online time once per hour (and on first run)
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # only query the weather every 10 minutes (and on first run) #> 600
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 60:
        try:
            value = pyportal.fetch()
            reload_count = reload_count + 1
            print("#%d: Response is" % reload_count, value)
            gfx.draw_display(value)
            gfx.clear_error()
            weather_refresh = time.monotonic()
        except RuntimeError as re:
            print("Some error occured, retrying! -", re)
            gfx.draw_error()
            continue
        except TimeoutError as te:
            print("Timeout - ", te)
            gfx.draw_error()
            continue

    # react to screen touch
    touch_point = touch.touch_point
    if touch_point:
        pyportal.play_file(beep_sound)
        gfx.touch(touch_point)

    # reach to touch but don't update everything on every loop
    if (not loop_refresh) or (time.monotonic() - loop_refresh) > updateTime:
        gfx.draw_time()

        gc.collect()
        end_mem = gc.mem_free()
        print("Free mem after updates: {}B".format(end_mem))
        print("This iteraton took {}B ".format(start_mem - end_mem))
        #time.sleep(updateTime)  # wait X seconds before updating anything again

    # update display based on how often the time widget needs to update
    updateTime = .5
    if gfx.time_widget.mode == "weekday":
        updateTime = 30