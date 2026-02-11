## Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, I2C
import i2c_lcd
import time

## HARDWARE STUFF
class LCDDisplay: 
    def __init__(self, scl_pin, sda_pin): ## LCD Display initiate
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        self.lcd = i2c_lcd.I2cLcd(self.i2c, 0x27, 2, 16)

    def write_at(self, col, row, message):
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

    def on(self): ##on
        self.buzzer.value(0)

    def off(self): ##off
        self.buzzer.value(1)


class Dial: 
    def __init__(self, dial_pin): ## variable resistor initiate
        self.var = ADC(Pin(dial_pin))
        self.var.ATTN_11DB 

    def read(self):
        return self.var.read()


## CONTROLLER
class BoomTimer:
    def __init__(self): # define where all the pins are
        self.lcd = LCDDisplay(22, 23)
        self.left_button = PushButton(12)
        self.right_button = PushButton(27)
        self.buzzer = Buzzer(14)
        self.dial = Dial(32)

        self.start_time = time.time() ## making a start time
        self.unit_mode = "seconds"  ##whatever normal unit is
        self.is_counting_down = False ## define counting down state
        self.terminated = False ## define terminated state

    ## changing variable resis from normal range to a defined range
    def remap(self, value, old_min, old_max, new_min, new_max):
        return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

    ## display stuff
    def update_time_display(self):
        elapsed_time = time.time() - self.start_time 
        ## defining units, digits, and time value for minutes and seconds for display
        if self.unit_mode == "minutes":
            time_value = elapsed_time / 60
            digit = "5.1f"
            unit = "min"
        else:
            time_value = elapsed_time
            digit = "7.0f"
            unit = "s"

        self.lcd.write_at(0, 0, f"Time:{time_value:{digit}}{unit}")

    def update_dial_display(self):
        ## defining the new ranges for var and its display
        raw_var = self.dial.read()
        mapped_value = self.remap(raw_var, 0, 4095, 0, 60)
        self.lcd.write_at(0, 1, f"V: {mapped_value:4.0f}s")
        return mapped_value

    ## what its doing
    def switch_unit(self): ## defining switching from seconds to minutes
        if self.unit_mode == "seconds":
            self.unit_mode = "minutes"
        else:
            self.unit_mode = "seconds"

    def start_countdown(self, seconds): 
        self.is_counting_down = True ## starting countdown but not terminated
        self.terminated = False
        self.lcd.clear()

        while seconds > 0:
            self.lcd.write_at(0, 0, f"Remaining: {seconds:4.0f}s") ## pretty display while it counts down
            time.sleep(1)
            seconds -= 1

            if self.right_button.is_pressed(): # if button is pressed before end of countdown, terminate and clear screen
                self.terminate()
                self.lcd.clear()
                return

        self.trigger_boom() ##set off the alarm

    def terminate(self): ## making terminate display and return to normal
        self.lcd.clear()
        self.lcd.write_at(0, 1, "TERMINATED!")
        self.terminated = True ## now terminate is true amd count down is false
        self.is_counting_down = False
        time.sleep(1)

    def trigger_boom(self): ## making boom display and alarm for end of countdown
        self.lcd.clear()
        self.lcd.write_at(0, 1, "BOOM!")
        self.buzzer.on() ## will stay on until reset

    def reset(self): ## reseting the system after the boom alarm 
        self.buzzer.off()
        self.start_time = time.time() ##restarting the timer
        self.is_counting_down = False
        self.lcd.clear()

    ## the main loop
    def run(self):
        while True:

            if not self.is_counting_down: ## normal time display and var display
                self.update_time_display()
                mapped_time = self.update_dial_display()

                if self.left_button.is_pressed(): ## switch to seconds or minutes when pushing left button
                    self.switch_unit()

                if self.right_button.is_pressed(): ## start countdown display when right button is pushed, also allows for terminate 
                    self.start_countdown(mapped_time)

            else:
                if self.right_button.is_pressed(): ## reset system at second r button push
                    self.reset()

            time.sleep(0.2) ## fast sleep time to get a quick button push


# run it 
timer = BoomTimer()
timer.run()