### Rebecca Martens and Kavin Bhuvan
from machine import Pin, ADC, I2C
import i2c_lcd
from hcsr04 import HCSR04 ## distance sensor
import time
import asyncio
import random
from bt_esp32_api import BLE

## display
display = I2C(0, scl=Pin(22), sda=Pin(23))
devices = display.scan()
print(devices)
lcd = i2c_lcd.I2cLcd(display, 0x27, 2, 16)

#bitmoji
led_icon = [
    0b00000,
    0b00000,
    0b01110,
    0b01110,
    0b01110,
    0b11111,
    0b01010,
    0b01010,
    ]
lcd.custom_char(1, led_icon)

#sensor scaling
preset_min = 0
preset_max = 4095

##rotary encoder
rot_1 = Pin(25, Pin.IN, Pin.PULL_UP)
rot_2 = Pin(26, Pin.IN, Pin.PULL_UP)
rot_button = Pin(12, Pin.IN, Pin.PULL_UP)
old = 1

## light sensor
light_sensor = ADC(Pin(35)) # wire connected to AO
light_sensor.atten(ADC.ATTN_11DB)

##led
led = Pin (19,Pin.OUT)
led.value(0)

green_led = Pin (18, Pin.OUT)
green_led.value(0)

#BLE device
DEVICE_NAME = "RebeKA"
SENSOR_TX_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"
SERVICE_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"

#BLE toggle switch
ble_switch = Pin(21, Pin.IN, Pin.PULL_UP)

#intialzing
min_val = preset_min
max_val = preset_max
mode = 'max'
lcd.clear()

sensor_reading = 4095 - light_sensor.read()
last_refresh = time.ticks_ms()

async def sensor_talk(ble, period_ms = 500 ):
    global sensor_reading, last_refresh, mode, min_val, max_val, old
    ble_timer = time.ticks_ms()
    
    while True:
        now_time = time.ticks_ms()
        #sensor reading range selection
        if time.ticks_diff(now_time, last_refresh) >= 500:
            sensor_reading = 4095 - light_sensor.read()
        #     print(sensor_reading) #actual
            icon = round(((sensor_reading-min_val) / (max_val-min_val))*16)
            icon = max(0,min(icon, 16))
        
            #led on / off setup
            if sensor_reading < min_val or sensor_reading > max_val:
                led.value(1)
            else:
                led.value(0)
            
            # Display sensor range using icon
            lcd.move_to(0,0)
            for i in range (icon):
                lcd.show_char(1)
            
            lcd.putstr((' ')*(16 - icon))
            last_refresh = now_time
        
        #min / max value toggle
        rot2_val = rot_2.value()
        if old != rot2_val:
            if rot2_val == 0: 
                if rot_1.value()==0:
                    mode = 'max'
                    print('right: max')
                else:
                    mode = 'min'
                    print('left: min')
                
                lcd.move_to(0,1)
                lcd.putstr(f'mode: {mode}    ')
                        
            old = rot2_val
                    

        if rot_button.value() == 0:
            lcd.clear()
            await asyncio.sleep_ms(500)
            
            if mode == 'min':
                min_val = sensor_reading
                lcd.move_to(0,1)
                lcd.putstr(f'min: {min_val}')
                print ('min')
            elif mode == 'max':
                max_val = sensor_reading
                lcd.move_to(0,1)
                lcd.putstr(f'max: {max_val}')
                print ('max')
        
        if ble_switch.value() == 0:
            green_led.value(1)
            if time.ticks_diff(now_time, ble_timer) >= period_ms:
                payload = f'{sensor_reading}, {min_val}, {max_val}\n'
                ble.send(payload.encode('utf-8'))
                ble_timer = now_time
            await asyncio.sleep_ms(20)
        else:
            green_led.value(0)
        

async def main():
    ble = BLE(name=DEVICE_NAME,
              service_uuid=SERVICE_UUID,
              tx_char_uuid=SENSOR_TX_UUID,
              adv_interval_us=250000)
    
    await ble.start_adv()
    print("BLE started, advertising ...")
    
    try:
        await sensor_talk(ble, period_ms=500)
    finally:
        await ble.stop()
        print("Stopped")
 
asyncio.run(main())