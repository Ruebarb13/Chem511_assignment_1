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
def long_alarm(alarm_duration):
    buzzer.value(0) #on
    utime.sleep(alarm_duration)
    buzzer.value(1) #off
    
## multiple beep alarm
def quick_bounce_alarm(alarm_duration):
    for i in range(5):
        buzzer.value(0) #on
        utime.sleep(alarm_duration)
        buzzer.value(1) #off
        utime.sleep(alarm_duration)
#       
      
high_reading = 0 # min
low_reading = 250 # max
start_time = time.time()

while True:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm ah')
    print(var.read())
    time_value = time.time() - start_time
    lcd.move_to(0, 0)
    lcd.putstr(f'{time_value}{distance:5.1f}') # no flicker from clear screen

    # update high
    if distance < 250 and distance > high_reading:
        high_reading = distance
    #if distance < 250 and distance > 15: # thresh of 15
        #long_alarm(1)

    # update low
    if distance < low_reading:
        low_reading = distance
    #if distance < 3: # thresh of 3
        #quick_bounce_alarm(0.1)

    lcd.move_to(0, 1)
    
    # dont print ugly 0 or 250
    if high_reading == 0 or low_reading == 250:
        lcd.putstr(f'H:{'--':>5} L:{'--':>5}') # no flicker from clear screen
    else:
        lcd.putstr(f'H:{high_reading:5.1f} L:{low_reading:5.1f}') # no flicker from clear screen

    # button to reset low/high values
    if l_button.value() == 0:
        high_reading = 0
        low_reading = 250
        lcd.clear()
        time_value = (time.time() - start_time) / 60
        lcd.move_to(0, 0)
        lcd.putstr(f'{time_value}{distance:5.1f}') # no flicker from clear screen
        lcd.move_to(0, 1)
        lcd.putstr(f'H:{'--':>5} L:{'--':>5}') # dont print ugly 0 or 250
        time.sleep(1)
        
    if r_button.value() == 0:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f'pushed right')
        time.sleep(1)
        
        
    time.sleep(1)