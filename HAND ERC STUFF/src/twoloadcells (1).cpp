#include <Wire.h>
#include <Adafruit_NAU7802.h>
#include <Arduino.h>

// Create two NAU7802 objects
Adafruit_NAU7802 nau1;
Adafruit_NAU7802 nau2;

void setupNAU(Adafruit_NAU7802 &nau);

void setup() {
  Serial.begin(115200);
  
  // Start both I2C buses
  Wire.begin();         // Default I2C (pins 18=SDA0, 19=SCL0 on Teensy 4.0)
  Wire.setClock(400000);

  Wire1.begin();        // Second I2C (pins 17=SDA1, 16=SCL1 on Teensy 4.0)
  Wire1.setClock(400000);

  // Initialize first load cell on Wire
  if (!nau1.begin(&Wire)) {
    Serial.println("NAU7802 #1 not found!");
    while (1);
  }

  // Initialize second load cell on Wire1
  if (!nau2.begin(&Wire1)) {
    Serial.println("NAU7802 #2 not found!");
    while (1);
  }

  // Setup for both
  setupNAU(nau1);
  setupNAU(nau2);

  Serial.println("Both load cells ready");
}

void setupNAU(Adafruit_NAU7802 &nau) {
  nau.setLDO(NAU7802_3V0);
  nau.setGain(NAU7802_GAIN_128);
  nau.setRate(NAU7802_RATE_320SPS);

  nau.calibrate(NAU7802_CALMOD_INTERNAL);
  nau.calibrate(NAU7802_CALMOD_OFFSET);

  // Prime ADC
  for (int i = 0; i < 10; i++) {
    while (!nau.available());
    nau.read();
  }
}

void loop() {
  if (nau1.available()) {
    int32_t reading1 = nau1.read();
    Serial.print("LC1: ");
    Serial.println(reading1);
  }

  if (nau2.available()) {
    int32_t reading2 = nau2.read();
    Serial.print("LC2: ");
    Serial.println(reading2);
  }

  delay(10);  // prevent spamming output
}
