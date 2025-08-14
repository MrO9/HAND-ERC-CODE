import serial
import time
import pandas as pd

# ----------- USER SETTINGS ------------
PORT = 'COM3'
BAUD = 115200
LOG_DURATION = 10  # seconds
OUTPUT_FILE = 'load_cell_data.xlsx'
# --------------------------------------

# Open serial connection
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()

print(f"Logging data from {PORT} for {LOG_DURATION} seconds...\n")

# Storage
timestamps = []
loadcell1 = []
loadcell2 = []

start = time.time()

while time.time() - start < LOG_DURATION:
    if ser.in_waiting:
        try:
            line = ser.readline().decode().strip()
            timestamp = time.time() - start

            if line.startswith("LC1:"):
                val1 = int(line.split(":")[1])
                loadcell1.append(val1)
                loadcell2.append(None)
                timestamps.append(timestamp)

            elif line.startswith("LC2:"):
                val2 = int(line.split(":")[1])
                loadcell2.append(val2)
                loadcell1.append(None)
                timestamps.append(timestamp)

        except Exception as e:
            continue

ser.close()

# Combine into DataFrame
df = pd.DataFrame({
    "Timestamp (s)": timestamps,
    "LC1": loadcell1,
    "LC2": loadcell2
})

# Forward fill missing values (optional)
df = df.sort_values("Timestamp (s)").reset_index(drop=True)
df = df.fillna(method='ffill')

# Save to Excel
df.to_excel(OUTPUT_FILE, index=False)
print(f"\nData saved to {OUTPUT_FILE}")
