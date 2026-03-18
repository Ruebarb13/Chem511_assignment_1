# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from time import sleep_ms
from machine import Pin
i = 0
led = Pin(2, Pin.OUT)
if i< 5:
    led.value(1)
    sleep_ms(200)
    led.value(0)
    sleep_ms(1000)
    i += 1
    print(i)