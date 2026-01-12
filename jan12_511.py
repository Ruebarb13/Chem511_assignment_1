from machine import Pin, I2C
import utime
import i2c_lcd

dennis = I2C(0, scl=Pin(23), sda=Pin(22))
devices = dennis.scan()
print(devices)

lcd = i2c_lcd.I2cLcd(dennis, 0x27, 2, 16)

#lcd.clear() ## CLEAR THE SCREEN

lcd.move_to(1,0) ## MOVE THE CURSOR TO FIRST LINE

lcd.putstr('guess what?') ## Print on screen

utime.sleep(1) ## TIME DELAY 

lcd.move_to(1,1) ## MOVE THE CURSOR TO SECOND LINE 

lcd.putstr('chicken butt') ## Print on screen

utime.sleep(1)

lcd.clear()

utime.sleep(1)

lcd.move_to(0,0)

#lcd.putstr('1234567891011121314151617181920212324252627282930')
lcd.putstr('1234567891011121xxxxxxxxxxxxxxxxxxxxxxxx6272829303132333')

# lcd.move_to(1,1)

#lcd.putstr('knock KNOCK')


