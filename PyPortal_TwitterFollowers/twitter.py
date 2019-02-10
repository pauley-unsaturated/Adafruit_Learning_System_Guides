"""
This example will access the twitter follow button API, grab a number like
the number of followers... and display it on a screen!
if you can find something that spits out JSON data, we can display it
"""
import time
import board
from digitalio import DigitalInOut, Direction
from adafruit_pyportal import PyPortal

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise


# Change this to your twitter username!
TWITTER_NAME = "adafruit"

# Set up where we'll be fetching data from
DATA_SOURCE = "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names="+TWITTER_NAME
DATA_LOCATION = [0, "followers_count"]

# determine the current working directory
# needed so we know where to find files
cwd = __file__.rsplit('/', 1)[0]
# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE, json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=cwd+"/twitter_background.bmp",
                    text_font=cwd+"/fonts/Collegiate-50.bdf",
                    text_position=(165, 140),
                    text_color=0xFFFFFF,
                    caption_text="www.twitter.com/"+TWITTER_NAME,
                    caption_font=cwd+"/fonts/Collegiate-24.bdf",
                    caption_position=(50, 200),
                    caption_color=0xFFFFFF,)

# track the last value so we can play a sound when it updates
last_value = 0

while True:
    try:
        value = pyportal.fetch()
        print("Response is", value)
        if last_value < value:  # ooh it went up!
            print("New follower!")
            pyportal.play_file(cwd+"/coin.wav")  # uncomment make a noise!
        last_value = value
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)

    time.sleep(60)  # wait a minute before getting again
