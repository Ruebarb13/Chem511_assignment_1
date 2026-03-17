import asyncio
from bt_python_api import BLEClient
import time

#the values should match with esp32 / thonny

SERVICE_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"
SENSOR_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"
DEVICE_NAME = "lalala"

def on_data(sender, data: bytes):
        try:
            signal = data.decode('utf-8').strip()            
            packets = signal.split(',')
            sensor_reading, min_val, max_val = int(packets[0]), int(packets[1]), int(packets[2])
            print (f'sensor: {sensor_reading}, min_value: {min_val}, max_value: {max_val}')
            time.sleep(0.2)
        except Exception:
            print("Raw:", data)

async def main():
    client = BLEClient(name=DEVICE_NAME,
                       service_uuids=[SERVICE_UUID],
                       connect_timeout=15.0,
                       scan_timeout=15.0
                       )
    try: 
        await client.connect()
        await client.start_notify(SENSOR_UUID, on_data)
        print("Listening... Press Ctrl+C to stop.")
        await asyncio.Event().wait()
    finally:
        await client.disconnect()

asyncio.run(main())
