### Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, PWM, DAC, I2C
import i2c_lcd
from hcsr04 import HCSR04 ## distance sensor
import time

## display
display = I2C(0, scl=Pin(22), sda=Pin(23))
devices = display.scan()
print(devices)
lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)

## buzzer
buzzer = Pin(14, Pin.OUT)
buzzer.value(1)

## distance sensor
sensor = HCSR04(trigger_pin=13, echo_pin=33)
distance = sensor.distance_cm()

## left button
l_button = Pin(12, Pin.IN, Pin.PULL_UP)

## right button
r_button = Pin(27, Pin.IN, Pin.PULL_UP)

## variable resistor
var = ADC(Pin(32)) # variable resistor connected to 32 pin 
var.ATTN_11DB # classic code

## light sensor
light_sensor = ADC(Pin(35)) # wire connected to AO (analog output)
light_sensor.ATTN_11DB

#lcd.putstr('pot: %d' % var.read())  # read the variable resistor dial
#print(var.read())  # read the variable resistor dial
#lcd.putstr('l_sens: %d' % (4095 - light_sensor.read())) # read the light sensor wavelength (REVERSE IT)

## long beep alarm
def boom_alarm(alarm_duration):
    buzzer.value(0) #on
    time.sleep(alarm_duration)
    buzzer.value(1) #off

# def for making variable resistor in seconds
def remap(value, var_min, var_max, new_min, new_max):
    return (value - var_min) * (new_max - new_min) / (var_max - var_min) + new_min

# def for making countdown clock
def countdown(seconds):
    while seconds > 0:
        lcd.move_to(0, 1)
        lcd.putstr(f"Remaining: {seconds:5.0f}s")
        time.sleep(1)
        seconds -= 1
    lcd.clear()
    lcd.move_to(0, 1)
    lcd.putstr('BOOM!')

start_time = time.time()
i = 0
r_button_pressed = False

while True:
    # determining counter time and the units
    if i == 0:
        time_value = time.time() - start_time
        unit = 's'
    elif i % 2 == 0:
        time_value = (time.time() - start_time)
        unit = 's'
    elif i % 2 > 0:
        time_value = (time.time() - start_time) / 60
        unit = 'min'
    time_value = time_value
    
    #configure correct digits for defined units (no ugly digit for seconds)
    if unit == 'min':
        digit = '5.1f'
    else:
        digit = '7.0f'
    
    # put time and units on display
    lcd.move_to(0, 0)
    lcd.putstr(f'Time:{time_value:{digit}}{unit}') # no flicker from clear screen
    
    # convert variable resistor into variable timer and display current setting on display
    raw_var = var.read()
    mapped_value = remap(raw_var, 0, 4095, 0, 60)
    lcd.move_to(0, 1)
    lcd.putstr(f'V2:{mapped_value:4.0f}s')
    
    # print on comp the time, variable resistor, and variable timer every second
    print(time_value, unit)
    print(var.read())
    print(mapped_value)
    
    # l_button pushed and we up count
    if l_button.value() == 0:
        i = i+1 
        print(time_value)
        
    # r_button pushed and we start countdown and turn on buzzer
    if r_button.value() == 0 and r_button_pressed == False:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f'Countdown')
        countdown(mapped_value)
        buzzer.value(0) #on
        r_button_pressed = True
        
                    
    # r_button is pushed again and we restart device/count and stop the buzzer
    if r_button.value() == 0 and r_button_pressed == True:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f'Restart')
        buzzer.value(1) #off
        r_button_pressed = False
        time.sleep(1)
        lcd.clear()
        start_time = time.time()
        
    time.sleep(1)