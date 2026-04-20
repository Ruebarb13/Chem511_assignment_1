#### Rebecca Martens & Kavin Bhuvan
# connecting esp and reg python
from serial import Serial
import time
import os

#4. Write a program that runs on your ESP32 and continuously streams light sensor data 
# to the serial port, i.e. using the print() command in microPython. Now write another 
# program in (regular) Python that runs on your computer that continuously reads those 
# sensor values. If the readings are below a threshold value, your computer's code should 
# do nothing. If they are above a certain value, it should print an alert.

PORT = 'COM3'
BAUD = 115200
high_limit = 3500

esp32 = Serial(port = PORT, baudrate = BAUD, timeout =1)
while True:
    response = esp32.readline().decode('utf-8').strip()
    if response.isnumeric():
        response = int(response)
        if response > high_limit:
            print ('ALERT - TOO BRIGHT!: ', response)

        else:
            os.system('cls') ## If the readings are below a threshold value, your computer's code should do nothing. 
            # i.e. this section prints nothing/ clears screen

        time.sleep(0.2)
    else:
        print ('ignored response:' ,response)

