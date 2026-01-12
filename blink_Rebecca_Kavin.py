# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from time import sleep_ms
from machine import Pin
import utime
i = 0

#led = Pin(2, Pin.OUT)
#while i<10:
#    led.value(1)
#    sleep_ms(200)
#    led.value(0)
#    sleep_ms(200)
#    i+=1
#    print(f"I'm smarter than Kavin {i}")
    
led = Pin(12, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
i=0
while i==0:
    if button.value()==0:
        led.value(1)
        #i+=1
        print(f"doo doo doo")
    else:
        led.value(0)
        utime.sleep(0.1)
        #i+=1
        print(f"I'm way smarter than Kavin {i}")
        
        
#while i<20:    
#    led.value(1)
#    sleep_ms(200)
#    led.value(0)
#    sleep_ms(200)
#    i+=1
#    print(f"I'm way smarter than Kavin {i}")
    

    