# Rebecca Martens and Kavin Bhuvan
from time import sleep_ms
import utime
from machine import Pin, ADC, I2C
import i2c_lcd

display = I2C(0, scl=Pin(25), sda=Pin(26))
devices = display.scan()
print(devices)

light_sensor = ADC(Pin(33))
light_sensor.ATTN_11DB

lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)
g_led = Pin(13, Pin.OUT)
g_led.value(0)

while True:      
    if light_sensor.read() > 2000: 
        g_led.value(1)
        lcd.move_to(0,0) 
        lcd.clear()
        lcd.putstr('LIGHT IS') 
        lcd.move_to(0,1) 
        lcd.putstr('ON! %d' % (4095 - light_sensor.read())) 
        utime.sleep(1)
    else:
        g_led.value(0)
        lcd.move_to(0,0) 
        lcd.clear()
        lcd.putstr('LIGHT IS') 
        lcd.move_to(0,1) 
        lcd.putstr('OFF! %d' % (4095 - light_sensor.read())) 
        utime.sleep(1)
        
    