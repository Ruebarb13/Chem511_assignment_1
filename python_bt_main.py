import asyncio
from bt_python_api import BLEClient

SERVICE_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
SENSOR_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"
DEVICE_NAME = "lalala"

def on_data(sender, data: bytes):
        try:
            print("Value:", int(data.decode().strip())) 
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
