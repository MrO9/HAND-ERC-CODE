import sys
import serial
import time
import numpy as np
from collections import deque
from PyQt5 import QtWidgets
import pyqtgraph as pg

# --- Serial Setup ---
PORT = 'COM3'      
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1) # Open serial port
ser.flushInput() # Clear any garbage in the serial buffer

# --- Plot Setup ---
WINDOW_DURATION = 45  # Display the last 120 seconds
MAX_POINTS = 320 * WINDOW_DURATION  # Max points to hold in buffer
BUFFER_TIME = deque(maxlen=MAX_POINTS) # Deque to store timestamps
BUFFER_VALUE = deque(maxlen=MAX_POINTS) # Deque to store converted force values (in N)

app = QtWidgets.QApplication([]) # Create GUI app
win = pg.GraphicsLayoutWidget(title="Live Load Cell Data") # Main plot window
plot = win.addPlot(title="Load Cell Reading") # Create plot inside window
plot.setLabel('bottom', 'Time', units='s')
plot.setLabel('left', 'Force', units='N') # Changed label from "ADC Value" to "Force"
real_curve = plot.plot() # Actual data that will be plotted in realtime
desired_curve = plot.plot()
plot.setXRange(0, WINDOW_DURATION, padding=0) # Set fixed x-range (scrolling window)

win.show()

# --- Timing Setup ---
start_time = time.time()
last_sample_time = start_time
sample_times = deque(maxlen=100)  # For calculating sampling rate

# --- Calibration values (from previous calibration script) ---
ZERO_OFFSET = 54084.25
NEWTONS_PER_COUNT = -0.000049



# # Time vector: 10 points per second (i.e., 100 ms interval)
# t = np.linspace(0, WINDOW_DURATION, WINDOW_DURATION * 10)

# # Piecewise force definition
# y = np.piecewise(
#     t,
#     [t < 5,
#      (t >= 5) & (t < 10),
#      (t >= 10) & (t < 15),
#      (t >= 15) & (t < 20),
#      (t >= 20) & (t < 25),
#      (t >= 25) & (t < 30),
#      (t >= 30) & (t < 35),
#      (t >= 35) & (t < 40),
#      t >= 40],
#     [
#         0,
#         lambda t: 0.1 * (t - 5),             # 0 to 0.5 ramp
#         0.5,
#         lambda t: -0.08 * (t - 15) + 0.5,     # 0.5 to 0.1 ramp
#         0.1,
#         lambda t: 0.08 * (t - 25) + 0.1,      # 0.1 to 0.5 ramp
#         0.5,
#         lambda t: -0.1 * (t - 35) + 0.5,      # 0.5 to 0 ramp
#         0
#     ]
# )

real_curve = plot.plot(pen=pg.mkPen('r', width=3)) 
# desired_curve.setData(t, y)

def update():
    global last_sample_time
    while ser.in_waiting: # While there are bytes in serial
        try:
            line = ser.readline().decode().strip() # Read serial line and turn bytes into string
            raw_adc = int(line) # Convert to int
            current_time = time.time() - start_time

            # Convert raw ADC to force in Newtons using calibration
            force = (raw_adc - ZERO_OFFSET) * NEWTONS_PER_COUNT

            BUFFER_TIME.append(current_time)
            BUFFER_VALUE.append(force)

            sample_times.append(time.time())
        except ValueError:
            continue  # Skip bad lines

    if len(BUFFER_TIME) > 0: # If BUFFER_TIME has elements in it
        real_curve.setData(BUFFER_TIME, BUFFER_VALUE) # Reset data in curve to current deques

        # Auto-scroll the x-axis
        if BUFFER_TIME[-1] > WINDOW_DURATION:
            plot.setXRange(BUFFER_TIME[-1] - WINDOW_DURATION, BUFFER_TIME[-1], padding=0)

        # Sampling rate display
        if len(sample_times) > 2:
            intervals = np.diff(sample_times)
            avg_rate = 1.0 / np.mean(intervals)
            win.setWindowTitle(f"Live Load Cell Data — {avg_rate:.1f} Hz")

timer = pg.QtCore.QTimer() # Timer to update plot
timer.timeout.connect(update) 
timer.start(10)  # 10 ms update interval (up to ~100 fps)

if __name__ == '__main__':
    sys.exit(app.exec_())

