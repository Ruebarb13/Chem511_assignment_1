### Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, PWM, DAC, I2C
import i2c_lcd
from hcsr04 import HCSR04 ## distance sensor
import utime

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
print('Distance:', distance, 'cm')

## button
button = Pin(12, Pin.IN, Pin.PULL_UP)

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
      
      
high_reading = 0 # min
low_reading = 250 # max

while True:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')

    lcd.move_to(0, 0)
    lcd.putstr(f'Distance:{distance:5.1f}') # no flicker from clear screen

    # update high
    if distance < 250 and distance > high_reading:
        high_reading = distance
        if high_reading > 50: # thresh of 50 
            long_alarm(1)

    # update low
    if distance < low_reading:
        low_reading = distance
        if low_reading < 3: # thresh of 3
            quick_bounce_alarm(0.1)

    lcd.move_to(0, 1)
    
    # dont print ugly 0 or 250
    if high_reading == 0 or low_reading == 250:
        lcd.putstr(f'H:{'--':>5} L:{'--':>5}') # no flicker from clear screen
    else:
        lcd.putstr(f'H:{high_reading:5.1f} L:{low_reading:5.1f}') # no flicker from clear screen

    # button to reset low/high values
    if button.value() == 0:
        high_reading = 0
        low_reading = 250
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f'Distance:{distance:5.1f}')
        lcd.move_to(0, 1)
        lcd.putstr(f'H:{'--':>5} L:{'--':>5}') # dont print ugly 0 or 250
        utime.sleep(1)
        
    utime.sleep(1)