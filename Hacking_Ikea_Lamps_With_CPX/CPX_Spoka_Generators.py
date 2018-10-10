import time

from adafruit_circuitplayground.express import cpx

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))

class ColorSequence:
    def __init__(self, colors):
        self.colors = colors
        self.index = 0

    def advance(self):
        cpx.pixels.fill(wheel(colors[self.index % 256]))
        self.index += 1

patterns = [
    ColorSequence(range(256)),  # rainbow_cycle
    ColorSequence([0]),  # red
    ColorSequence([10]),  # orange
    ColorSequence([30]),  # yellow
    ColorSequence([85]),  # green
    ColorSequence([137]),  # cyan
    ColorSequence([170]),  # blue
    ColorSequence([213]),  # purple
    ColorSequence([0, 10, 30, 85, 137, 170, 213]),  # party mode
]

heart_rates = [0, 0.5, 1.0]

heart_rate = 0
last_heart_beat = time.monotonic()
next_heart_beat = last_heart_beat + heart_rate

pattern = None

cpx.detect_taps = 2
cpx.pixels.brightness = 0.2

i = 0
current_speed_index = 0
while True:
    now = time.monotonic()

    if cpx.tapped or pattern is None:
        pattern = patterns[i % len(patterns)]
        i += 1

    if cpx.shake(shake_threshold=20):
        current_speed_index += 1
        heart_rate = heart_rates[current_speed_index % len(heart_rates)]
        last_heart_beat = now
        next_heart_beat = last_heart_beat + heart_rate

    if now >= next_heart_beat:
        pattern.advance()
        last_heart_beat = now
        next_heart_beat = last_heart_beat + heart_rate
