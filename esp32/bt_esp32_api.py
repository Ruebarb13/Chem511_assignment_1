"""
ESP32 BLE API - Beginner Guide
==============================

What this file does
-------------------
This file gives you one simple class: BLE.

Use BLE to:
- Advertise your ESP32 as a BLE device.
- Send bytes from ESP32 to phone/PC (TX characteristic).
- Receive bytes from phone/PC to ESP32 (RX characteristic).

You can use it without deep knowledge of asyncio or multithreading.


Very simple asyncio idea
------------------------
- async def: a function that can pause and continue later.
- await: pause here until this step is done.
- While paused, other BLE tasks can keep running.

You do NOT need threads for normal use of this file.


BLE object and key methods
--------------------------
Create:
    ble = BLE(...)

Start advertising:
    await ble.start_adv()

Send data to central:
    ble.send(b"hello")

Receive data from central (option 1: callback):
    def on_rx(data, conn):
        print("RX:", data)

    ble = BLE(..., on_rx=on_rx)

Receive data from central (option 2: manual loop):
    while True:
        data, conn = await ble.receive()
        print("RX:", data)

Stop BLE:
    await ble.stop()


Important rule
--------------
Choose only ONE RX style:
1) on_rx callback
or
2) await ble.receive() loop

Do not use both at the same time.


Default connection logs
-----------------------
If you do not pass on_connect/on_disconnect, default functions are used:
- on connect -> prints Connected: ...
- on disconnect -> prints Disconnected


Example A: Send sensor value every 2 seconds
---------------------------------------------
    import asyncio
    from random import randint
    from esp32_blue_simple_api import BLE

    async def main():
        ble = BLE(name="ESP32")
        await ble.start_adv()

        try:
            while True:
                value = randint(0, 100)
                ble.send(str(value).encode())
                print("TX:", value)
                await asyncio.sleep(2)
        finally:
            await ble.stop()

    asyncio.run(main())


Example B: Receive LED command with callback
--------------------------------------------
    import asyncio
    from machine import Pin
    from esp32_blue_simple_api import BLE

    led = Pin(2, Pin.OUT)

    def on_rx(data, conn):
        if data == b"1":
            led.value(1)
            print("LED ON")
        elif data == b"0":
            led.value(0)
            print("LED OFF")
        else:
            print("Unknown:", data)

    async def main():
        ble = BLE(name="ESP32", on_rx=on_rx)
        await ble.start_adv()
        try:
            await asyncio.Event().wait()  # run forever
        finally:
            await ble.stop()

    asyncio.run(main())


Troubleshooting
---------------
- If you see no connection:
  Check name and UUIDs match on both ESP32 and client.
- If receive does not work:
  Make sure central writes to RX characteristic UUID.
- If send does not show on client:
  Make sure client subscribed to TX notifications.
"""


import asyncio
import aioble
import bluetooth


def default_on_connect(conn):
    print("Connected:", conn.device if hasattr(conn, "device") else conn)

def default_on_disconnect(conn):
    print("Disconnected")


class BLE:
    """
    Minimal BLE communication API for ESP32 MicroPython using aioble.

    Responsibilities:
      - Create a custom BLE service with a TX (notify/read) and RX (write) characteristic.
      - Advertise and hold connections.
      - Let user code SEND arbitrary bytes and RECEIVE arbitrary bytes.

    This class deliberately knows nothing about sensors, LEDs, or app semantics.

    TX = characteristic used by the peripheral to notify the central (downlink to central)
    RX = characteristic written by the central (uplink to peripheral)
    """

    def __init__(
        self,
        *,
        name: str = "ESP32",
        service_uuid: str = '19b10000-e8f2-537e-4f6c-d104768a1214',
        tx_char_uuid: str = '19b10001-e8f2-537e-4f6c-d104768a1214',
        rx_char_uuid: str = '19b10002-e8f2-537e-4f6c-d104768a1214',
        adv_interval_us: int = 250_000,
        on_connect=default_on_connect,
        on_disconnect=default_on_disconnect,
        on_rx=None,  # optional callback: on_rx(data: bytes, connection)
    ):
        self.name = name
        self.adv_interval_us = adv_interval_us
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._on_rx = on_rx

        # UUIDs and GATT
        self._svc_uuid = bluetooth.UUID(service_uuid)
        self._tx_uuid = bluetooth.UUID(tx_char_uuid)
        self._rx_uuid = bluetooth.UUID(rx_char_uuid)

        self._service = aioble.Service(self._svc_uuid)
        # TX: peripheral -> central (notify); readable so central can read initial value
        self.tx_char = aioble.Characteristic(
            self._service, self._tx_uuid, read=True, notify=True
        )
        # RX: central -> peripheral (write). capture=True returns (connection, data)
        self.rx_char = aioble.Characteristic(
            self._service, self._rx_uuid, read=True, write=True, notify=False, capture=True
        )

        aioble.register_services(self._service)
        try:
            self.tx_char.write(b"", send_update=False)
            self.rx_char.write(b"", send_update=False)
        except Exception as e:
            print("Initial char write error:", e)

        self._tasks = []
        self._running = False
        self._connection = None
        self._use_callback_rx = on_rx is not None

    # -------------------- public API --------------------
    def is_connected(self) -> bool:
        return self._connection is not None

    async def start_adv(self):
        if self._running:
            return
        self._running = True
        self._tasks = [
            asyncio.create_task(self._advertise_task()),
        ]
        if self._use_callback_rx:
            self._tasks.append(asyncio.create_task(self._rx_task()))

    async def stop(self):
        if not self._running:
            return
        self._running = False
        for t in self._tasks:
            try:
                t.cancel()
            except Exception:
                pass
        await asyncio.sleep_ms(100)
        self._tasks = []

    def send(self, data: bytes):
        """Notify the central with arbitrary bytes on TX characteristic."""
        try:
            self.tx_char.write(data, send_update=True)
        except Exception as e:
            print("send() error:", e)

    async def receive(self):
        """Await one write to the RX characteristic and return (data: bytes, connection).

        Note: Do not use this concurrently with the on_rx callback mode.
        """
        connection, data = await self.rx_char.written()
        return data, connection

    # -------------------- internal ----------------------
    async def _advertise_task(self):
        # Serially wait for connections. Do not advertise while connected.
        while self._running:
            try:
                async with await aioble.advertise(
                    self.adv_interval_us, name=self.name, services=[self._svc_uuid]
                ) as connection:
                    self._connection = connection
                    if self._on_connect:
                        try:
                            self._on_connect(connection)
                        except Exception as e:
                            print("on_connect callback error:", e)

                    await connection.disconnected()

                    if self._on_disconnect:
                        try:
                            self._on_disconnect(connection)
                        except Exception as e:
                            print("on_disconnect callback error:", e)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print("advertise_task error:", e)
            finally:
                self._connection = None
                await asyncio.sleep_ms(100)

    async def _rx_task(self):
        # Dispatch writes to the optional on_rx callback
        while self._running:
            try:
                connection, data = await self.rx_char.written()
                if self._on_rx:
                    try:
                        self._on_rx(data, connection)
                    except Exception as e:
                        print("on_rx callback error:", e)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print("rx_task error:", e)
            await asyncio.sleep_ms(10)

