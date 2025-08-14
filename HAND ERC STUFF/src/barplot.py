import sys
import serial
import time
import numpy as np
from PyQt5 import QtWidgets
import pyqtgraph as pg

# --- Serial Setup ---
PORT = 'COM10'
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()

# --- Plot Setup ---
app = QtWidgets.QApplication([])
win = pg.GraphicsLayoutWidget(title="Live Force Bar")
plot = win.addPlot()
#plot.setLabel('left', 'Force', units='N')
plot.setXRange(-1, 1)  # Fixed x-range so bar stays centered
plot.setYRange(0, 15)  # Adjusted a bit above 10 to leave room above horizontal line
plot.hideAxis('left')
plot.hideAxis('bottom')  # Hide x-axis

# Single force bar at x = 0
bar = pg.BarGraphItem(x=[0], height=[0], width=0.5, brush='r')
plot.addItem(bar)

# Add a horizontal line at y = 10
target_line = pg.InfiniteLine(pos=10, angle=0, pen=pg.mkPen('g', width=6))
plot.addItem(target_line)

win.show()

# --- Calibration values ---
ZERO_OFFSET = 54084.25
NEWTONS_PER_COUNT = -0.000049

# --- Sampling Rate Setup ---
sample_times = []

scale = [10/1, 10/2, 10/4, 10/8, 10/16]

def update():
    global bar, sample_times

    while ser.in_waiting:
        try:
            line = ser.readline().decode().strip()
            raw_adc = int(line)

            # Convert raw ADC to force
            force = (raw_adc - ZERO_OFFSET) * NEWTONS_PER_COUNT
            force = max(0, force)  # Clip negative forces to zero if desired

            scaled_force = force/scale[1]

            # Update bar height
            bar.setOpts(height=[scaled_force])

            # --- Sampling Rate Calculation ---
            now = time.time()
            sample_times.append(now)
            if len(sample_times) > 100:  # Keep only last 100 samples
                sample_times.pop(0)

            if len(sample_times) > 1:
                intervals = np.diff(sample_times)
                avg_rate = 1.0 / np.mean(intervals)
                win.setWindowTitle(f"Live Force Bar — {avg_rate:.1f} Hz")

        except ValueError:
            continue  # Ignore bad serial lines

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)

if __name__ == '__main__':
    sys.exit(app.exec_())
