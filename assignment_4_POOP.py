''' 
Assignement 4 objectives:
Using a combination of LCD display, buzzer/LED, potentiometer, and push buttons, make a count-down timer.

a) Have the first push button toggle between setting the minutes vs seconds. [2 marks]

b) The value of the integer (minutes or seconds) is set by the potentiometer. [2 marks]

c) The second push button starts the countdown, and then silences the alarm after the time has elapsed. [2 marks]

d) Create a UML diagram for your code. [2 marks]

'''
'''
Possible class structure:
    Class for LCD display
    Class for reading dial value
    class for reading the push button toggle between minutes and seconds
    class for boom timer



'''
'''
Model - minute/ seconds, boom timer, 
View - lCD, buzzer
Control - Potentiometer, buttons
'''



from machine import Pin, ADC, PWM, DAC, I2C
import i2c_lcd
from hcsr04 import HCSR04 ## distance sensor
import time

class LCDDisplay:
    def __init__(self, scl_pin, sda_pin):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        # devices = self.display.scan()
        # print(devices)
        self.lcd = i2c_lcd.I2cLcd(self.i2c, 0x27, 2, 16)

    def write(self, message):
        self.lcd.putstr(message)

    def move(self, col, row):
        self.lcd.move_to(col, row)

    def clear(self):
        self.lcd.clear()


class PushButton:
    def __init__(self, pin_number):
        ## button
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_UP)
   
        

class Buzzer:
    def __init__(self, pin_number = 14):
        self.buzzer = Pin(pin_number, Pin.OUT)
        self.off()

    def off(self):
        self.buzzer.value(1)

    def on(self):
        self.buzzer.value(0) 
     
       
class DistanceSensor:
    def __init__(self, trigger_pin = 13, echo_pin = 33):
        self.sensor = HCSR04(trigger_pin, echo_pin)

    def distance(self):
        return self.sensor.distance_cm()    

class Dial:
    def __init__(self, pin = 32):
                ## variable resistor
        self.var = ADC(Pin(pin)) # variable resistor connected to 32 pin 
        self.var.ATTN_11DB # classic code

class LightSensor:
    def __init__(self, pin = 35):
        ## light sensor
        self.light_sensor = ADC(Pin(pin)) # wire connected to AO (analog output)
        self.light_sensor.ATTN_11DB


class BoomTimer:
       
    
    
    def __init__(self):
        
        self.lcd = LCDDisplay(22, 23)
        self.l_button = PushButton(12)
        self.r_button = PushButton(27)
        self.buzzer = Buzzer(14)    
        self.pot = Dial(32)
        self.buzzer.off()
    def beep(self, duration):
        self.buzzer.on()
        time.sleep(duration)
        self.buzzer.off()
    
    def remap(self, value, var_min, var_max, new_min, new_max):
        return (value - var_min) * (new_max - new_min) / (var_max - var_min) + new_min

    def countdown(self, seconds):
        while seconds > 0:
            self.lcd.move(0, 0)
            self.lcd.putstr(f"Remaining: {seconds:5.0f}s")
            time.sleep(1)
            seconds -= 1
        self.lcd.clear()
        self.lcd.move(0, 1)
        self.lcd.write('BOOM!')

    def main(self):
        self.start_time = time.time()
        i = 0
        r_button_pressed = False
        while True:

             # determining counter time and the units
            unit = 's' if i % 2 == 0 else 'min' # toggle between seconds and minutes
            time_value = time_value

            #configure correct digits for defined units (no ugly digit for seconds)
            if unit == 'min':
                digit = '5.1f'
            else:
                digit = '7.0f'

            self.lcd.move(0, 0)
            self.lcd.write(f'Time:{time_value:{digit}}{unit}') # no flicker from clear screen

            raw_var = self.pot.var.read()
            mapped_value = self.remap(raw_var, 0, 4095, 0, 60)
            self.lcd.move(0, 1)
            self.lcd.write(f'V2: {mapped_value:4.0f}{unit}')

            # print on comp the time, variable resistor, and variable timer every second
            print(time_value, unit)
            print(self.pot.var.read())
            print(mapped_value)

            
        # l_button pushed and we up count
        
            if self.l_button.button.value() == 0:
                i = i+1 
                print(time_value)
                
            # r_button pushed and we start countdown and turn on buzzer
            if self.r_button.button.value() == 0 and r_button_pressed == False:
                self.lcd.clear()
                self.lcd.move(0, 0)
                self.lcd.write(f'Countdown')
                self.countdown(mapped_value)
                self.buzzer.on() #on
                r_button_pressed = True
                
                            
            # r_button is pushed again and we restart device/count and stop the buzzer
            if self.r_button.button.value() == 0 and r_button_pressed == True:
                self.lcd.clear()
                self.lcd.move(0, 0)
                self.lcd.write(f'Restart')
                self.buzzer.off() #off
                r_button_pressed = False
                time.sleep(0.2)
                self.lcd.clear()
                self.start_time = time.time()
                
            time.sleep(0.2)


timer = BoomTimer()
timer.main()






