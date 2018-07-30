#!/usr/bin/env python
import time

import RPi.GPIO as GPIO

colors = [0xFF00, 0x00FF, 0x0FF0, 0xF00F]
pins = (11, 12)  # pins is a dict

GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
GPIO.setup(pins, GPIO.OUT)  # Set pins' mode is output
GPIO.output(pins, GPIO.LOW)  # Set pins to LOW(0V) to off led

p_R = GPIO.PWM(pins[0], 1000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins[1], 1000)

p_R.start(0)  # Initial duty Cycle = 0(leds off)
p_G.start(0)


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setColor(col):  # For example : col = 0x1122
    R_val = col >> 8
    G_val = col & 0x00FF

    R_val = list(map(R_val, 0, 255, 0, 100))
    G_val = list(map(G_val, 0, 255, 0, 100))

    p_R.ChangeDutyCycle(R_val)  # Change duty cycle
    p_G.ChangeDutyCycle(G_val)


def setRedGreenColor(R_val):
    G_val = 255 - R_val
    R_val = list(map(R_val, 0, 255, 0, 100))
    G_val = list(map(G_val, 0, 255, 0, 100))
    p_R.ChangeDutyCycle(R_val)  # Change duty cycle
    p_G.ChangeDutyCycle(G_val)


def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(0.5)


def loop2():
    colors = list(range(0, 256))
    sleep_for = 0.01
    while True:
        for i in colors:
            setRedGreenColor(i)
            time.sleep(sleep_for)
        for i in colors[::-1]:
            setRedGreenColor(i)
            time.sleep(sleep_for)


def destroy():
    p_R.stop()
    p_G.stop()
    GPIO.output(pins, GPIO.LOW)  # Turn off all leds
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        loop2()
    except:
        destroy()
