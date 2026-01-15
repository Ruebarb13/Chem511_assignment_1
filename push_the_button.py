# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from time import sleep_ms
from machine import Pin
import utime
i = 0
from machine import Pin, I2C
import utime
import i2c_lcd

dennis = I2C(0, scl=Pin(23), sda=Pin(22))
devices = dennis.scan()
print(devices)

lcd = i2c_lcd.I2cLcd(dennis, 0x27, 2, 16)
    
led = Pin(12, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_UP)
i=0
while i==0:
    if button.value()==0:
        led.value(1)
        #i+=1
        print(f"doo doo doo")
        #lcd.clear() ## CLEAR THE SCREEN

        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE
        lcd.clear()
        lcd.putstr('CONGRATS YOU') ## Print on screen

        #utime.sleep(1) ## TIME DELAY 

        lcd.move_to(1,1) ## MOVE THE CURSOR TO SECOND LINE 

        lcd.putstr('PUSHED IT!') ## Print on screen

        utime.sleep(1)


    else:
        led.value(0)
        utime.sleep(0.1)
        #i+=1
        print(f"I'm way smarter than Kavin {i}")
        lcd.clear()
        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE

        lcd.putstr('PUSH THE') ## Print on screen

        #utime.sleep(1) ## TIME DELAY 

        lcd.move_to(0,1) ## MOVE THE CURSOR TO SECOND LINE 

        lcd.putstr('BUTTON!') ## Print on screen

        utime.sleep(2)
        
        
#while i<20:    
#    led.value(1)
#    sleep_ms(200)
#    led.value(0)
#    sleep_ms(200)
#    i+=1
#    print(f"I'm way smarter than Kavin {i}")