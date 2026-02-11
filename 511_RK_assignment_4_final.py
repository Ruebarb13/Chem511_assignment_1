## Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, PWM, DAC, I2C
import i2c_lcd
import time

class LCDDisplay:
    def __init__(self, scl_pin, sda_pin): ## LCD Display initiate
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.lcd = i2c_lcd.I2cLcd(self.i2c, 0x27, 2, 16)
        
    def write_at(self,col, row, message):
        self.lcd.move_to(col, row)
        self.lcd.putstr(message)
        
    def clear(self):
        self.lcd.clear()

class PushButton:
    def __init__(self, push_pin): ## button initiate
        self.button = Pin(push_pin, Pin.IN, Pin.PULL_UP)
    def is_pressed(self):
        return self.button.value() == 0
   
class Buzzer:
    def __init__(self, buzz_pin): ## buzzer initiate
        self.buzzer = Pin(buzz_pin, Pin.OUT)
        self.off()
        
    def off(self):
        self.buzzer.value(1)
        
    def on(self):
        self.buzzer.value(0)    

class Dial:
    def __init__(self, dial_pin): ## variable resistor initiate
        self.var = ADC(Pin(dial_pin))
        self.var.ATTN_11DB 

class BoomTimer:
    def __init__(self): # define where all the pins are
        self.lcd = LCDDisplay(22, 23)
        self.l_button = PushButton(12)
        self.r_button = PushButton(27)
        self.buzzer = Buzzer(14)    
        self.pot = Dial(32)
        self.buzzer.off()
        
    def beep(self, duration): # defining buzzer on/off and sleep times
        self.buzzer.on()
        time.sleep(duration)
        self.buzzer.off()
        
    def remap(self, value, var_min, var_max, new_min, new_max): ## change units of variable resistor to seconds
        return (value - var_min) * (new_max - new_min) / (var_max - var_min) + new_min
    
    def boom_display(self): ##put boom on screen
        self.lcd.write_at(0, 1, 'BOOM!')
        
    def countdown(self, seconds): ## display countdown timer on screen or abort if terminated
        self.terminated = False
        while seconds > 0:
            self.lcd.write_at(0, 0, f"Remaining: {seconds:4.0f}s")
            time.sleep(1)
            seconds -= 1
            if self.r_button.is_pressed():
                self.lcd.clear()
                self.lcd.write_at(0, 1, 'TERMINATED!')
                self.terminated = True
                time.sleep(1)
                return
        self.lcd.clear()
        self.boom_display()
        self.buzzer.on()

    def main(self): ## main function which changes time between s/min, reads the variable resistor and starts/restarts the timer
        self.start_time = time.time()
        i = 0
        r_button_pressed = False
        while True:

            # determining counter time and the units
            unit = 's' if i % 2 == 0 else 'min' # toggle between seconds and minutes
            time_value = time.time() - self.start_time

            #configure correct digits for defined units (no ugly digit for seconds)
            if unit == 'min':
                digit = '5.1f'
                time_value = (time_value/60)
            else:
                digit = '7.0f'
                time_value = time_value
            self.lcd.write_at(0, 0, f'Time:{time_value:{digit}}{unit}') 
            
            # read the variable resistor and convert the min/max to min/max in seconds
            raw_var = self.pot.var.read()
            mapped_value = self.remap(raw_var, 0, 4095, 0, 60)
            
            # display varaible seconds on screen
            self.lcd.write_at(0, 1, f'V: {mapped_value:4.0f}s')

            # print on comp the time, variable resistor, and variable timer every second
            print(time_value, unit)
            print(self.pot.var.read())
            print(mapped_value)

            # l_button pushed and we up the count
            if self.l_button.is_pressed():
                i = i+1 
                print(time_value)
                
            # r_button pushed and we start countdown and turn on buzzer
            if self.r_button.is_pressed() and r_button_pressed == False:
                self.lcd.clear()
                self.lcd.write_at(0, 0, f'Countdown')
                self.countdown(mapped_value)
                r_button_pressed = True
                
            # continue to display boom until restart
            while self.r_button.button.value() == 1 and r_button_pressed == True:
                if self.terminated == False:
                    self.boom_display()
                if self.r_button.is_pressed():
                    break
                             
            # r_button is pushed again and we restart device/count and stop the buzzer
            if self.r_button.is_pressed() and r_button_pressed == True:
                self.lcd.clear()
                self.lcd.write_at(0, 0, f'Restart')
                self.buzzer.off() #off
                r_button_pressed = False
                time.sleep(1)
                self.lcd.clear()
                self.start_time = time.time()
                
            time.sleep(0.2)

#call it 
timer = BoomTimer()
timer.main()