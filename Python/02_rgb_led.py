#!/usr/bin/env python
import random
import time
from itertools import tee

import RPi.GPIO as GPIO

try:
    
except ImportError:
    izip = zip

colors = [0xFFFFFF, 0xFF0000, 0x00FF00, 0x712400, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]
colors.append(colors[0])
R = 11
G = 12
B = 13


def random_color():
    color = random.choice(colors)
    while True:
        next_color = random.choice(list({color} ^ set(colors)))
        old_color = color
        color = next_color
        yield old_color, next_color


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def setup(Rpin, Gpin, Bpin):
    global pins
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)  # Set pins' mode is output
        GPIO.output(pins[i], GPIO.HIGH)  # Set pins to high(+3.3V) to off led

    p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)

    p_R.start(100)  # Initial duty Cycle = 0(leds off)
    p_G.start(100)
    p_B.start(100)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def off():
    for i in pins:
        GPIO.output(pins[i], GPIO.HIGH)  # Turn off all leds


def hex_to_rgb(col):
    R_val = (col & 0xff0000) >> 16
    G_val = (col & 0x00ff00) >> 8
    B_val = (col & 0x0000ff) >> 0
    return R_val, G_val, B_val


def _set_color(r, g, b):
    p_R.ChangeDutyCycle(100 - r)
    p_G.ChangeDutyCycle(100 - g)
    p_B.ChangeDutyCycle(100 - b)


def setColor(col):  # For example : col = 0x112233
    _set_color(*[list(map(c, 0, 255, 0, 100)) for c in hex_to_rgb(col)])


def fade_to_color(color, new_color):
    color = [list(map(c, 0, 255, 0, 100)) for c in hex_to_rgb(color)]
    new_color = [list(map(c, 0, 255, 0, 100)) for c in hex_to_rgb(new_color)]
    while color != new_color:
        for i, col in enumerate(new_color):
            if color[i] > col:
                color[i] -= 1
            elif color[i] < col:
                color[i] += 1
        _set_color(*color)
        time.sleep(random.uniform(0.001, .2))


def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(1)


def loop2():
    while True:
        for old, new in random_color():
            print(("{} => {}".format(hex(old), hex(new))))
            fade_to_color(old, new)
            time.sleep(.2)


def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    off()
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        setup(R, G, B)
        loop2()
    except:
        destroy()
