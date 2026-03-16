### Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, I2C
import i2c_lcd
from hcsr04 import HCSR04 ## distance sensor
import time

## display
display = I2C(0, scl=Pin(22), sda=Pin(23))
devices = display.scan()
print(devices)
lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)

#bitmoji
heart = [
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000,
    0b00000,
    ]
led = [
    0b00000,
    0b00000,
    0b01110,
    0b01110,
    0b01110,
    0b11111,
    0b01010,
    0b01010,
    ]
lcd.custom_char(0,heart)
lcd.custom_char(1, led)
#sensor scaling
preset_min = 0
preset_max = 4095

##rotary encoder
rot_1 = Pin(25, Pin.IN, Pin.PULL_UP)
rot_2 = Pin(26, Pin.IN, Pin.PULL_UP)
select_button = Pin(27, Pin.OUT)
debounce = 0.2
rot_button = Pin(12, Pin.IN, Pin.PULL_UP)

## light sensor
light_sensor = ADC(Pin(35)) # wire connected to AO
light_sensor.atten(ADC.ATTN_11DB)

#intialzing
min_val = preset_min
max_val = preset_max

while True:
    sensor_reading = 4095 - light_sensor.read()
    print(sensor_reading) #actual
    
    icon = round(((sensor_reading-min_val) / (max_val-min_val))*16)
    print(icon)
    icon = max(min_val,min(icon, 16))
    lcd.clear()
    lcd.move_to(0,0)
    for i in range (icon):
        lcd.show_char(0)
    time.sleep(0.5)




