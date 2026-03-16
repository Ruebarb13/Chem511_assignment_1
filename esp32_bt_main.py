import asyncio
import random
from bt_esp32_api import BLE

SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"
SENSOR_TX_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
DEVICE_NAME = "lalala"

async def sensor_task(ble, period_ms=1000):
    while True:
        value = random.randint(0,100) # TODO Connect this to a sensor instead of yielding random numbers
        payload = str(value).encode("UTF-8")
        ble.send(payload)
        print(value)
        await asyncio.sleep_ms(period_ms)

async def main():
    ble = BLE(name=DEVICE_NAME,
              service_uuid=SERVICE_UUID,
              tx_char_uuid=SENSOR_TX_UUID,
              adv_interval_us=250000)
    
    await ble.start_adv()
    print("BLE started, advertising ...")
    
    try:
        await sensor_task(ble, period_ms=1000)
    finally:
        await ble.stop()
        print("Stopped")
        
asyncio.run(main())
