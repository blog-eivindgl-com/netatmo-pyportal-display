import sys
import board
import time
from adafruit_pyportal import PyPortal
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
DATA_SOURCE = "http://192.168.1.19:8080/api/display"
DATA_LOCATION = []

# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(
                    url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)
gfx = netatmo_display.Netatmo_Display(pyportal.splash)
localtile_refresh = None
weather_refresh = None
mode = "weekday"
while True:
    # only query the online time once per hour (and on first run)
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue

    # only query the weather every 10 minutes (and on first run)
    if (not weather_refresh) or (time.monotonic() - weather_refresh) > 600:
        try:
            value = pyportal.fetch()
            print("Response is", value)
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

    gfx.draw_time()
    updateTime = .5
    if mode == "weekday":
        updateTime = 30

    time.sleep(updateTime)  # wait X seconds before updating anything again
