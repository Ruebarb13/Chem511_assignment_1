## Rebecca Martens and Kavin Bhuvan

import asyncio
import time
import matplotlib.pyplot as pyplot
from bt_python_api import BLEClient

SERVICE_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"
SENSOR_UUID = "1f7f71c9-f157-44fe-9fc4-163931e34db2"
DEVICE_NAME = "RebeKA"

# storage for plotting
times = []
values = []
current_min = None
current_max = None
start_time = time.time()

def on_data(sender, data: bytes):
    global current_min, current_max, current_sens

    try:
        signal = data.decode("utf-8").strip()
        packets = signal.split(",")

        sensor_reading, min_val, max_val = int(packets[0]), int(packets[1]), int(packets[2])

        elapsed = time.time() - start_time

        # put new values/readings in the lists
        times.append(elapsed) 
        values.append(sensor_reading)
        # update the new min and max if changed
        current_min = min_val
        current_max = max_val
        current_sens = sensor_reading


        print(f"sensor: {sensor_reading}, min_value: {min_val}, max_value: {max_val}")
    except Exception:
        print("Raw:", data)

async def plot_live():
    pyplot.ion()  ## interactive to change in real time for new min and max 
    fig, ax = pyplot.subplots(figsize=(8, 4))
    line, = ax.plot([], [])
    
    max_text = ax.text(0.01, 0.95, '', color='k', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0'))
    min_text = ax.text(0.01, 0.90, '', color='k', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0'))
    sensor_text = ax.text(0.01, 0.85, '', color='k', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0'))
    warning_text = ax.text(0.01, 0.05, '', color='r', transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0'))
    
    last_min = None
    last_max = None

    ax.set_xlabel("time (s)")
    ax.set_ylabel("sensor reading")
    ax.set_title("live light sensor data")

    while True:
        if times and values:
            line.set_xdata(times)
            line.set_ydata(values)
            sensor_text.set_text(f'Sens: {current_sens}')
            ax.set_xlim(min(times), max(times) if max(times) > 1 else 1)
            
            if current_min is not None and current_max is not None:
                if current_sens < current_min:
                    warning_text.set_text('WARNING: below minimum')
                elif current_sens > current_max:
                    warning_text.set_text('WARNING: above maximum')
                else:
                    warning_text.set_text('')
            else:
                warning_text.set_text('')

            if current_min is not None and current_max is not None:
                ax.set_ylim(current_min, current_max) ##setting new range if we have a new min or max 

                if current_min != last_min or current_max != last_max:
                    max_text.set_text(f'Max: {current_max}')
                    min_text.set_text(f'Min: {current_min}')
                    last_min = current_min
                    last_max = current_max

            else:
                ax.set_ylim(0, 4095)

                if last_min != 0 or last_max != 4095:
                    max_text.set_text('Max: 4095')
                    min_text.set_text('Min: 0')
                    last_min = 0
                    last_max = 4095

            ax.autoscale_view(scalex=False, scaley=False)#update view limits and dont autoscale to fit data

            fig.canvas.draw() #redraw all the data when updated, in interactive mode it preps the figure for display
            fig.canvas.flush_events()

        await asyncio.sleep(0.1)

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
        await asyncio.gather(plot_live(),
                             asyncio.Event().wait()
                             )
    finally:
        await client.disconnect()

asyncio.run(main())
