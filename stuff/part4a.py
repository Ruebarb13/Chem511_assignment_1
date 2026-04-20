#### Rebecca Martens & Kavin Bhuvan
# connecting esp and reg python
from machine import Pin, ADC, I2C
import i2c_lcd
import time

#4. Write a program that runs on your ESP32 and continuously streams light sensor data 
# to the serial port, i.e. using the print() command in microPython. Now write another 
# program in (regular) Python that runs on your computer that continuously reads those 
# sensor values. If the readings are below a threshold value, your computer's code should 
# do nothing. If they are above a certain value, it should print an alert.

## display
display = I2C(0, scl=Pin(22), sda=Pin(23))
devices = display.scan()
print(devices)
lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)

## light sensor
light_sensor = ADC(Pin(35)) # wire connected to AO
light_sensor.ATTN_11DB

while True:
    light_reading = (4095 - light_sensor.read())
    print(light_reading)
    lcd.move_to(0, 0)
    lcd.putstr(f'light: {light_reading:5.0f}')
    time.sleep(0.4)

