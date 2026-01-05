# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from time import sleep_ms
from machine import Pin
i = 0

led = Pin(2, Pin.OUT)
while True:
    led.value(1)
    sleep_ms(200)
    led.value(0)
    sleep_ms(200)