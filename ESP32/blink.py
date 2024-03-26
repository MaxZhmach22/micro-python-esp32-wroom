import machine
import socket
import time

led = machine.Pin(4, machine.Pin.OUT)
delay = 0.2
blinks_count = 8

def blink_led():
    led.value(False)
    for n in range(blinks_count):
        led.value(not led.value())
        time.sleep(delay)