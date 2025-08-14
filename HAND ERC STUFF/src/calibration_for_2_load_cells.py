import serial
import time
import numpy as np

# ----------- USER SETTINGS ------------
PORT = 'COM3'
BAUD = 115200

KNOWN_MASS_KG_1 = 0.02  # Known mass for Load Cell 1
KNOWN_MASS_KG_2 = 0.02  # Known mass for Load Cell 2


G = 9.81  # Acceleration due to gravity (m/s^2)
CALIBRATION_DURATION = 10  # Seconds to average data
# --------------------------------------

def read_average_dual(seconds, label):
    readings_1 = []
    readings_2 = []

    print(f"\n{label} for {seconds} seconds...")


    start = time.time()
    while time.time() - start < seconds:
        if ser.in_waiting:
            try:
                line = ser.readline().decode().strip()

                if line.startswith("LC1:"):
                    val1 = int(line.split(":")[1])
                    readings_1.append(val1)

                elif line.startswith("LC2:"):
                    val2 = int(line.split(":")[1])
                    readings_2.append(val2)

            except Exception as e:
                continue

    if not readings_1 or not readings_2:
        raise RuntimeError("No valid readings collected for one or both load cells.")

    avg1 = np.mean(readings_1)
    avg2 = np.mean(readings_2)

    print(f"Average LC1 ({label}): {avg1:.2f}")
    print(f"Average LC2 ({label}): {avg2:.2f}")

    return avg1, avg2

# Open serial connection
ser = serial.Serial(PORT, BAUD, timeout=1)
ser.flushInput()

print("===== DUAL LOAD CELL CALIBRATION =====")

# Step 1: Zero / No load
input("Step 1: Remove all weight from both load cells. Press Enter to continue")
zero_avg1, zero_avg2 = read_average_dual(CALIBRATION_DURATION, "Zero load")

# Step 2: Known mass
input(f"\nStep 2: Place {KNOWN_MASS_KG_1:.3f} kg on LC1 and {KNOWN_MASS_KG_2:.3f} kg on LC2. Press Enter to continue")
load_avg1, load_avg2 = read_average_dual(CALIBRATION_DURATION, "Known load")

# Compute calibration
delta1 = load_avg1 - zero_avg1
delta2 = load_avg2 - zero_avg2

force1 = KNOWN_MASS_KG_1 * G
force2 = KNOWN_MASS_KG_2 * G

npc1 = force1 / delta1
npc2 = force2 / delta2

print("\n===== CALIBRATION COMPLETE =====")
print(f"LC1 Zero offset: {zero_avg1:.2f}")
print(f"LC1 Known load avg: {load_avg1:.2f}")
print(f"LC1 Raw diff: {delta1:.2f}")
print(f"LC1 Force: {force1:.3f} N")
print(f"LC1 Newtons per count: {npc1:.6f} N/count")

print(f"\nLC2 Zero offset: {zero_avg2:.2f}")
print(f"LC2 Known load avg: {load_avg2:.2f}")
print(f"LC2 Raw diff: {delta2:.2f}")
print(f"LC2 Force: {force2:.3f} N")
print(f"LC2 Newtons per count: {npc2:.6f} N/count")

ser.close()

