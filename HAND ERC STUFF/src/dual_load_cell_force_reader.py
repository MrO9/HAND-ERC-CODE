import serial
import time
import pandas as pd

# ----------- USER SETTINGS ------------
PORT = 'COM3'
BAUD = 115200
DISPLAY_INTERVAL = 0  # seconds between display updates
OUTPUT_FILE = 'load_cell_forces.xlsx'

# -------- Calibration Constants --------
ZERO_OFFSET_1 = -1257.00
ZERO_OFFSET_2 = 953.44

NPC_1 = -0.000058
NPC_2 =  0.000081
# --------------------------------------

def calculate_force(raw, zero_offset, npc):
    return (raw - zero_offset) * npc

# Open serial connection
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()

print("===== DUAL LOAD CELL FORCE MONITOR =====")
print("Press Ctrl+C to stop\n")

# List to store synced readings
data_log = []  # list of dicts with time, LC1, LC2

# Buffers for unsynced readings
pending_lc1 = None
pending_lc2 = None
last_timestamp = None

start_time = time.time()

try:
    while True:
        if ser.in_waiting:
            try:
                line = ser.readline().decode("utf-8").strip("b'rn\\")
                now = time.time()
                elapsed = now - start_time

                if line.startswith("LC1:"):
                      raw1 = int(line.split(":")[1])
                      force1 = calculate_force(raw1, ZERO_OFFSET_1, NPC_1)
                      pending_lc1 = force1
                      last_timestamp = elapsed
                      print(f"LC1 Raw: {raw1} → Force: {force1:.3f} N")

                if line.startswith("LC2:"):
                    raw2 = int(line.split(":")[1])
                    force2 = calculate_force(raw2, ZERO_OFFSET_2, NPC_2)
                    pending_lc2 = force2
                    last_timestamp = elapsed
                    print(f"LC2 Raw: {raw2} → Force: {force2:.3f} N")

                # Log only when both values are available
                if pending_lc1 is not None and pending_lc2 is not None:
                    data_log.append({
                        "Time (s)": last_timestamp,
                        "LC1 Force (N)": pending_lc1,
                        "LC2 Force (N)": pending_lc2
                    })
                    pending_lc1 = None
                    pending_lc2 = None

                time.sleep(DISPLAY_INTERVAL)

            except Exception:
                continue

except KeyboardInterrupt:
    print("\nStopped.")

    end_time = time.time()
    window_start = end_time - 30  # last 30 seconds

    # Average LC1
    recent_lc1 = [d["LC1 Force (N)"] for d in data_log if start_time + d["Time (s)"] >= window_start]
    avg_lc1 = sum(recent_lc1) / len(recent_lc1) if recent_lc1 else None

    # Average LC2
    recent_lc2 = [d["LC2 Force (N)"] for d in data_log if start_time + d["Time (s)"] >= window_start]
    avg_lc2 = sum(recent_lc2) / len(recent_lc2) if recent_lc2 else None

    print("\n===== AVERAGE FORCE OVER LAST 30 SECONDS =====")
    if avg_lc1 is not None:
        print(f"LC1 Average Force: {avg_lc1:.3f} N")
    else:
        print("LC1: No data in the last 30 seconds.")
    if avg_lc2 is not None:
        print(f"LC2 Average Force: {avg_lc2:.3f} N")
    else:
        print("LC2: No data in the last 30 seconds.")

    # Save to Excel
    df = pd.DataFrame(data_log)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"\nData saved to '{OUTPUT_FILE}'.")

finally:
    ser.close()
