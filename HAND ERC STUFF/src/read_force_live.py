import serial
import time

# ----------- USER SETTINGS ------------
PORT = 'COM10'
BAUD = 115200
DISPLAY_INTERVAL = 0.2  # seconds
# -------- Calibration Constants --------
ZERO_OFFSET = 1659.95       # Replace with your zero-load average
NEWTONS_PER_COUNT = 0.000320  # Replace with your calibration value (N/count)
# --------------------------------------

def calculate_force(raw_value):
    return (raw_value - ZERO_OFFSET) * NEWTONS_PER_COUNT

# Open serial connection
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()

print("Reading load cell force in real-time. Press Ctrl+C to stop.\n")

try:
    while True:
        if ser.in_waiting:
            try:
                line = ser.readline().decode().strip()

                if line.startswith("LC1:"):
                    raw = int(line.split(":")[1])
                    force = calculate_force(raw)
                    print(f"LC1 Raw: {raw} → Force: {force:.2f} N")

                elif line.startswith("LC2:"):
                    raw = int(line.split(":")[1])
                    force = calculate_force(raw)
                    print(f"LC2 Raw: {raw} → Force: {force:.2f} N")

                time.sleep(DISPLAY_INTERVAL)

            except ValueError:
                continue  # skip bad lines

except KeyboardInterrupt:
    print("\nStopped.")
finally:
    ser.close()
