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
led_icon = [
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
lcd.custom_char(1, led_icon)

#sensor scaling
preset_min = 0
preset_max = 4095

##rotary encoder
rot_1 = Pin(25, Pin.IN, Pin.PULL_UP)
rot_2 = Pin(26, Pin.IN, Pin.PULL_UP)
rot_button = Pin(12, Pin.IN, Pin.PULL_UP)
debounce = 0.5
old = 1

## light sensor
light_sensor = ADC(Pin(35)) # wire connected to AO
light_sensor.atten(ADC.ATTN_11DB)

##led
led = Pin (27,Pin.OUT)
led.value(0)


#intialzing
min_val = preset_min
max_val = preset_max
mode = 'max'
lcd.clear()


last_refresh = time.ticks_ms()
while True:
    #sensor reading range selection
    if time.ticks_diff(time.ticks_ms(), last_refresh) >= 500:
        sensor_reading = 4095 - light_sensor.read()
    #     print(sensor_reading) #actual
        icon = round(((sensor_reading-min_val) / (max_val-min_val))*16)
        icon = max(0,min(icon, 16))
    
        #led on / off setup
        if sensor_reading < min_val or sensor_reading > max_val:
            led.value(1)
        else:
            led.value(0)
        
        # Display sensor range using icon
        lcd.move_to(0,0)
        for i in range (icon):
            lcd.show_char(1)
        
        lcd.putstr((' ')*(16-icon))
        last_refresh = time.ticks_ms()
    
    #min / max value toggle
    if old != rot_2.value():
        if rot_2.value() == 0: 
            if rot_1.value()==0:
                mode = 'max'
                print('right: max')
            else:
                mode = 'min'
                print('left: min')
            
            lcd.move_to(0,1)
            lcd.putstr(f'mode: {mode}    ')
                    
        old = rot_2.value()
                

    if rot_button.value() == 0:
        lcd.clear()
        time.sleep(debounce)
        
        if mode == 'min':
            min_val = sensor_reading
            lcd.move_to(0,1)
            lcd.putstr(f'min: {min_val}')
            print ('min')
        elif mode == 'max':
            max_val = sensor_reading
            lcd.move_to(0,1)
            lcd.putstr(f'max: {max_val}')
            print ('max')
