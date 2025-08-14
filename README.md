Overview

During my time at HAND ERC, I worked with Adafruit microcontrollers connected to load cells to measure forces across various transmission testbeds. This README outlines the setup, calibration, and testing process used to calculate force efficiency.

**Hardware Setup:**

Ensure the load cells are properly connected to the Adafruit devices.

Connect the Adafruit devices to the Teensy microcontroller.

Connect the Teensy to your computer.

**Software Setup:**
Install and set up Visual Studio.

Write your calibration code, or use the provided calibration script.

**Calibration Procedure:**

Offset measurement – With no weight on the load cells, record the offset value.

Scaling factor – Place a known weight (e.g., 20 g) on the load cells to determine the Newton-per-count scaling factor.

**Testing Procedure:**

Place your transmission module between the two load cells.

Route a tendon through the system.

Secure both ends of the tendon to the load cells using a knot or copper crimp.

**Data Collection:**
Record both input and output forces.

Calculate force efficiency:
=
Efficiency=
Input Force/Output Force
	​


Average multiple trials to determine the overall force efficiency.

Notes

Repeat calibration and testing as needed for consistent results.

Ensure secure connections to avoid noise in the force readings.
