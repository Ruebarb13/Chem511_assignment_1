from time import sleep_ms
import utime
from machine import Pin, ADC, I2C
import i2c_lcd

display = I2C(0, scl=Pin(25), sda=Pin(26))
devices = display.scan()
print(devices)

light_sensor = ADC(Pin(33)) # wire connected to AO (analog output)
light_sensor.ATTN_11DB

lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)
r_led = Pin(12, Pin.OUT)
g_led = Pin(13, Pin.OUT)
l_button = Pin(14, Pin.IN, Pin.PULL_UP)
r_button = Pin(27, Pin.IN, Pin.PULL_UP)

while True:
    if l_button.value()==0:
        g_led.value(1)
        r_led.value(0)
        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE
        lcd.clear()
        lcd.putstr('CONGRATS YOU') ## Print on screen
        #utime.sleep(1) ## TIME DELAY 
        lcd.move_to(1,1) ## MOVE THE CURSOR TO SECOND LINE 
        lcd.putstr('PUSHED LEFT!') ## Print on screen
        utime.sleep(1)
        
    elif r_button.value()==0:
        g_led.value(1)
        r_led.value(0)
        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE
        lcd.clear()
        lcd.putstr('CONGRATS YOU') ## Print on screen
        #utime.sleep(1) ## TIME DELAY 
        lcd.move_to(0,1) ## MOVE THE CURSOR TO SECOND LINE 
        lcd.putstr('PUSHED RIGHT!') ## Print on screen
        utime.sleep(1)
        
    elif light_sensor.read() > 2000: # reversed 
        g_led.value(1)
        r_led.value(0)
        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE
        lcd.clear()
        lcd.putstr('IT IS REAL') ## Print on screen
        #utime.sleep(1) ## TIME DELAY 
        lcd.move_to(0,1) ## MOVE THE CURSOR TO SECOND LINE 
        lcd.putstr('DARK! %d' % (4095 - light_sensor.read())) ## Print on screen
        utime.sleep(1)   
        
    else:
        g_led.value(0)
        r_led.value(1)
        utime.sleep(0.1)
        lcd.clear()
        lcd.move_to(0,0) ## MOVE THE CURSOR TO FIRST LINE
        lcd.putstr('PUSH A') ## Print on screen
        #utime.sleep(1) ## TIME DELAY 
        lcd.move_to(0,1) ## MOVE THE CURSOR TO SECOND LINE
        lcd.putstr('BUTTON!') ## Print on screen
        utime.sleep(1)
    