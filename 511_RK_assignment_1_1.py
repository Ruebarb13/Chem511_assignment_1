# Rebecca Martens and Kavin Bhuvan
from time import sleep_ms
import time
from machine import Pin, I2C
import i2c_lcd

display = I2C(0, scl=Pin(25), sda=Pin(26))
devices = display.scan()
print(devices)

lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)
r_led = Pin(12, Pin.OUT)
g_led = Pin(13, Pin.OUT)
l_button = Pin(14, Pin.IN, Pin.PULL_UP)

# intializing
last_press_time = 0
debounce_interval = 20  # ms
button_pressed = False
start_timer = 0
r_led.value(0)
g_led.value(0)

print("Starting...")

while True:

    if l_button.value() == 0 and button_pressed == False:
        now_time = time.ticks_ms()
        if time.ticks_diff(now_time, last_press_time) > debounce_interval:
            start_timer = now_time
            button_pressed = True
            last_press_time = now_time

    elif l_button.value() == 1 and button_pressed == True:
        end_timer = time.ticks_ms()
        button_pressed = False

        press_time = time.ticks_diff(end_timer, start_timer)
        print("Runtime:", press_time)
        
        if press_time < 1000:
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr('short press')
            print("short press")
        else:
            lcd.clear()
            lcd.move_to(0,0)
            lcd.putstr('long press')
            print("long press")

    sleep_ms(10)