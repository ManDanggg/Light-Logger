"""Live light logger: reads an Arduino over serial, plots raw and smoothed
light levels in real time, prints an alert when it gets dark, and saves
every reading to a CSV file when the plot window is closed."""

import time

import matplotlib.pyplot as plt
import numpy as np
import serial
from matplotlib.animation import FuncAnimation

PORT = "COM11"        # Windows: check Arduino IDE > Tools > Port. Mac: "/dev/cu.usbmodem..."
BAUD = 9600          # must match Serial.begin() in the Arduino sketch
WINDOW = 200         # readings shown on screen (200 x 0.1 s = 20 seconds)
SMOOTH = 10          # moving average size
THRESHOLD = 600     # "dark" level; match the Arduino sketch

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)              # opening the port resets the Arduino; let it restart
ser.reset_input_buffer()   # throw away anything sent during the restart

readings = np.full(WINDOW, np.nan)   # NaN = no data yet, so nothing is drawn
log = []                             # every reading, saved to CSV at the end
start = time.time()
was_dark = False


def read_new_values():
    """Read every complete line waiting in the serial buffer."""
    values = []
    while ser.in_waiting:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line.isdigit():           # skip partial or garbled lines
            values.append(int(line))
    return values


def moving_average(data, n):
    """Average of each group of n neighboring readings."""
    return np.convolve(data, np.ones(n) / n, mode="valid")


fig, ax = plt.subplots()
raw_line, = ax.plot([], [], label="Raw", alpha=0.4)
avg_line, = ax.plot([], [], label=f"Moving average ({SMOOTH})", linewidth=2)
ax.axhline(THRESHOLD, linestyle="--", color="gray", label="Dark threshold")
ax.set_xlim(0, WINDOW)
ax.set_ylim(0, 1023)
ax.set_xlabel("Sample (newest on the right)")
ax.set_ylabel("analogRead value (0 to 1023)")
ax.set_title("Live light level")
ax.legend(loc="upper left")


def update(frame):
    global readings, was_dark

    new = read_new_values()
    for value in new:
        log.append((time.time() - start, value))
    if new:
        # Add new readings on the right, drop the oldest on the left
        readings = np.concatenate([readings, new])[-WINDOW:]

    raw_line.set_data(np.arange(WINDOW), readings)
    avg = moving_average(readings, SMOOTH)
    avg_line.set_data(np.arange(SMOOTH - 1, WINDOW), avg)

    # Alert once each time the smoothed value crosses into "dark"
    is_dark = avg[-1] < THRESHOLD
    if is_dark and not was_dark:
        print(f"Alert: it got dark (smoothed reading {avg[-1]:.0f})")
    was_dark = is_dark

    return raw_line, avg_line


ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)
plt.show()   # blocks until you close the plot window

ser.close()
if log:
    np.savetxt("light_log.csv", np.array(log), delimiter=",",
               header="seconds,reading", comments="", fmt=["%.2f", "%d"])
    print(f"Saved {len(log)} readings to light_log.csv")
