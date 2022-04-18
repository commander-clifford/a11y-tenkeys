# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# RaspberryPi Pico RP2040 Mechanical Keyboard

import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

print("---Pico Pad Keyboard---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# list of pins to use (skipping GP15 on Pico because it's funky)
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

# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ BELOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ #
# -_-_-_-_-_-_-_-_-_-_ CHANGE THE KEYBOARD BUTTONS -_-_-_-_-_-_-_-_-_-_ #
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ BELOW -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ #
keymap = {
    (0): (KEY, (Keycode.GUI, Keycode.C)),
    (1): (KEY, (Keycode.GUI, Keycode.V)),
    (2): (KEY, [Keycode.THREE]),
    (3): (KEY, [Keycode.FOUR]),
    (4): (KEY, [Keycode.FIVE]),

    (5): (MEDIA, ConsumerControlCode.VOLUME_DECREMENT),
    (6): (MEDIA, ConsumerControlCode.VOLUME_INCREMENT),
    (7): (KEY, [Keycode.R]),
    (8): (KEY, [Keycode.G]),
    (9): (KEY, [Keycode.B])
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

while True:
    for button in range(10):
        if switch_state[button] == 0:
            if not switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.press(*keymap[button][1])
                    else:
                        cc.send(keymap[button][1])
                except ValueError:  # deals w six key limit
                    pass
                switch_state[button] = 1

        if switch_state[button] == 1:
            if switches[button].value:
                try:
                    if keymap[button][0] == KEY:
                        kbd.release(*keymap[button][1])

                except ValueError:
                    pass
                switch_state[button] = 0

    time.sleep(0.01)  # debouncer