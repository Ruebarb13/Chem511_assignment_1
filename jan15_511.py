import utime
import time
import i2c_lcd
from time import sleep_ms
from machine import Pin, ADC, I2C
#  CONTROL # TO COMMENT OUT
# setup
potentiometer = ADC(Pin(32)) # variable resistor connected to 32 pin 
potentiometer.ATTN_11DB # classic code
i2c_device = I2C(0, scl=Pin(23), sda=Pin(22)) # wires connected to associated pins
lcd = i2c_lcd.I2cLcd(i2c_device, 0x27, 2, 16)
light_sensor = ADC(Pin(33)) # wire connected to AO (analog output)
light_sensor.ATTN_11DB

while True:
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('pot: %d' % potentiometer.read())  # read the variable resistor dial
    lcd.move_to(0,1)
    lcd.putstr('l_sens: %d' % (4095 - light_sensor.read())) # read the light sensor wavelength (REVERSE IT)
    time.sleep(0.5)


