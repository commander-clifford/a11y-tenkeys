"""
SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
SPDX-License-Identifier: MIT
RaspberryPi Pico RP2040 Mechanical Keyboard

https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/consumer_control_code.html
https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/mouse.html
https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html
"""
 
import time
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_display_shapes.circle import Circle
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

displayio.release_displays()

i2c = busio.I2C(scl=board.GP17, sda=board.GP16)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)

# Draw a label
text = "Hello World!"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
)
splash.append(text_area)

time.sleep(1)

bg_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x000000 # black is OLED pixel off

bg_sprite = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette, x=0, y=0)
splash.append(bg_sprite)

print("---Pico Pad Keyboard---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

pins = (
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15
)

MEDIA = 1
KEY = 2
TYPE = 3
BLANK = 4
"""
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ BELOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
-_-_-_-_-_-_-_-_-_-_ CHANGE THE KEYBOARD BUTTONS -_-_-_-_-_-_-_-_-_-_
-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ BELOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
"""
current_menu = 2 # Menu 1 (0)
keymap = {
    # Menu 1 (0)
    (0): (KEY, "One", [Keycode.ONE]),
    (1): (KEY, "Two", [Keycode.TWO]),
    (2): (KEY, "Three", [Keycode.THREE]),
    (3): (KEY, "Four", [Keycode.FOUR]),
    (4): (KEY, "Five", [Keycode.FIVE]),

    (5): (TYPE, "Hello", ("Hello World!")),
    (6): (TYPE, "Hey", ("Hey")),
    (7): (KEY, "Select", [Keycode.OPTION, Keycode.SHIFT, Keycode.LEFT_ARROW]),
    (8): (KEY, "Copy", [Keycode.GUI, Keycode.C]),
    (9): (KEY, "Paste", [Keycode.GUI, Keycode.V]),

    # Menu 2 (1)
    (10): (KEY, "A", [Keycode.A]),
    (11): (KEY, "B", [Keycode.B]),
    (12): (KEY, "C", [Keycode.C]),
    (13): (KEY, "D", [Keycode.D]),
    (14): (KEY, "E", [Keycode.E]),

    (15): (KEY, "Left", [Keycode.LEFT_ARROW]),
    (16): (KEY, "Right", [Keycode.RIGHT_ARROW]),
    (17): (KEY, "Up", [Keycode.UP_ARROW]),
    (18): (KEY, "Down", [Keycode.DOWN_ARROW]),
    (19): (KEY, "Select", [Keycode.OPTION, Keycode.SHIFT, Keycode.RIGHT_ARROW]),

    # Menu 3 (2)
    (20): (MEDIA, "Vol -", ConsumerControlCode.VOLUME_DECREMENT),
    (21): (MEDIA, "Vol +", ConsumerControlCode.VOLUME_INCREMENT),
    (22): (MEDIA, "Mute", ConsumerControlCode.MUTE), 
    (23): (MEDIA, "Vol -", ConsumerControlCode.VOLUME_DECREMENT), 
    (24): (MEDIA, "Vol +", ConsumerControlCode.VOLUME_INCREMENT), 

    (25): (MEDIA, ">=", ConsumerControlCode.PLAY_PAUSE), 
    (26): (MEDIA, ">", ConsumerControlCode.SCAN_NEXT_TRACK), 
    (27): (MEDIA, "<", ConsumerControlCode.SCAN_PREVIOUS_TRACK), 
    (28): (MEDIA, "Screen -", ConsumerControlCode.BRIGHTNESS_DECREMENT), 
    (29): (MEDIA, "Screen +", ConsumerControlCode.BRIGHTNESS_INCREMENT), 
}
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ ABOVE -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ #
# -_-_-_-_-_-_-_-_-_-_ CHANGE THE KEYBOARD BUTTONS -_-_-_-_-_-_-_-_-_-_ #
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ ABOVE -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ #

switches = []
for i in range(len(pins)):
    switch = DigitalInOut(pins[i])
    switch.direction = Direction.INPUT
    switch.pull = Pull.UP
    switches.append(switch)

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

"""
Build UI (List of Button Functions)
"""
def build_menu(menu):
    for i in range(len(pins)):

        if i < 5:
            cx = 4
            x = 10
            y=(i*12)+4
        else:
            cx = 68
            x = 74
            y=((i-5)*12)+4

        text_area = label.Label(
            terminalio.FONT, text=keymap[i+(menu*10)][1], color=0xFFFFFF, x=x, y=y
        )
        
        circle = Circle(cx, y, 2, fill=0x000000, outline=0xFFFFFF)

        splash.append(text_area)
        splash.append(circle)
    
    return

def toggle_dot_label(i, io):

    print("keypress")
    print(i)
    print(io)

    if i < 5:
        x = 4
        y=(i*12)+4
    else:
        x = 68
        y=((i-5)*12)+4

    if io == 1:
        fill=0xFFFFFF
    else:
        fill=0x000000

    circle = Circle(x, y, 2, fill=fill, outline=0xFFFFFF)
    
    splash.append(circle)

    return

def toggle_to_menu(x):
    current_menu = x
    return

build_menu(current_menu)

while True:
    for button in range(10):
        key = button + (current_menu*10)
        if switch_state[button] == 0:
            if not switches[button].value:
                toggle_dot_label(button, 1)
                try:
                    if keymap[key][0] == KEY:
                        kbd.press(*keymap[key][2])
                    elif keymap[key][0] == TYPE:
                        layout.write(keymap[key][2])
                    else:
                        cc.send(keymap[key][2])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1
                
        if switch_state[button] == 1:
            if switches[button].value:
                toggle_dot_label(button, 0)
                try:
                    if keymap[key][0] == KEY:
                        kbd.release(*keymap[key][2])
                except ValueError:
                    pass
                switch_state[button] = 0
                

    time.sleep(0.01)  # debouncer

