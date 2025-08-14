// #include <Arduino.h>

// // put function declarations here:
// //int myFunction(int, int);

// #include "Adafruit_NAU7802.h"

//   Adafruit_NAU7802 nau1;
//   Adafruit_NAU7802 nau2;

//   //Define pins connected to Teensy board
//   const uint8_t DATA_PIN = 18;
//   const uint8_t CLOCK_PIN = 19;
//   const int NUM_SAMPLES = 1000;
//   int32_t unloadedAverage = 0;
//   int32_t loadedAverage = 0;
//   int32_t readingSum = 0;
//   int sampleCount = 0;
//   unsigned long startTime = 0;
//   float KNOWN_WEIGHT = 250;

//   float getForce();

//   bool unloadedDone = false;
//   bool loadedDone = false;
//   float off1;
//   float off2;
//   float c_f1;
//   float c_f2;

//   float getForce(float c, float offset, Adafruit_NAU7802 nau){

  
//   int32_t reading = nau.read();
//   float weight = static_cast<float>(reading - offset) / c;
//   return (weight * 9.81) / 1000;
// }

//   int average(Adafruit_NAU7802 nau){
//   int value = 0;
//   for(int i= 0; i<1000; i++){
//     value += nau.read();
//   }
//   return value/1000;

// }

// void which_loadcell(Adafruit_NAU7802 nau, float off, float c_f){
//    while(!Serial){}
//     Serial.begin(115200);
//     Serial.println("Adafruit NAU7802.");


//     if(!nau.begin()){
//       Serial.println("Failed to find NAU7802.");
//       while(1) delay(10);
//     }
//     Serial.println("Found NAU7802.");

//     nau.setLDO(NAU7802_3V0);
//     Serial.print("LDO voltage set to ");
//     switch (nau.getLDO()) {
//       case NAU7802_4V5:  Serial.println("4.5V"); break;
//       case NAU7802_4V2:  Serial.println("4.2V"); break;
//       case NAU7802_3V9:  Serial.println("3.9V"); break;
//       case NAU7802_3V6:  Serial.println("3.6V"); break;
//       case NAU7802_3V3:  Serial.println("3.3V"); break;
//       case NAU7802_3V0:  Serial.println("3.0V"); break;
//       case NAU7802_2V7:  Serial.println("2.7V"); break;
//       case NAU7802_2V4:  Serial.println("2.4V"); break;
//       case NAU7802_EXTERNAL:  Serial.println("External"); break;
//       }

//     nau.setGain(NAU7802_GAIN_128);
//     Serial.print("Gain set to ");
//     switch (nau.getGain()) {
//       case NAU7802_GAIN_1:  Serial.println("1x"); break;
//       case NAU7802_GAIN_2:  Serial.println("2x"); break;
//       case NAU7802_GAIN_4:  Serial.println("4x"); break;
//       case NAU7802_GAIN_8:  Serial.println("8x"); break;
//       case NAU7802_GAIN_16:  Serial.println("16x"); break;
//       case NAU7802_GAIN_32:  Serial.println("32x"); break;
//       case NAU7802_GAIN_64:  Serial.println("64x"); break;
//       case NAU7802_GAIN_128:  Serial.println("128x"); break;
//     }

//     nau.setRate(NAU7802_RATE_320SPS);
//     Serial.print("Conversion rate set to ");
//     switch (nau.getRate()) {
//       case NAU7802_RATE_10SPS:  Serial.println("10 SPS"); break;
//       case NAU7802_RATE_20SPS:  Serial.println("20 SPS"); break;
//       case NAU7802_RATE_40SPS:  Serial.println("40 SPS"); break;
//       case NAU7802_RATE_80SPS:  Serial.println("80 SPS"); break;
//       case NAU7802_RATE_320SPS:  Serial.println("320 SPS"); break;
//     }

//     for (uint8_t i = 0; i < 10; i++){
//       while (!nau.available()) delay(1);
//       nau.read();
//     }

//     while (!nau.calibrate(NAU7802_CALMOD_INTERNAL)){
//       Serial.println("Failed to calibrate internal offset, retrying.");
//       delay(1000);
//     }
//     Serial.println("Calibrated internal offset.");

//     while (!nau.calibrate(NAU7802_CALMOD_OFFSET)){
//       Serial.println("Failed to calibrate system offset, retrying.");
//     }
//     Serial.println("Calibrated system offset.");

//      off = average(nau);
//      Serial.println(off);
//      delay(20000);
//      c_f = average(nau);
//      c_f -= off;
//      c_f /= 30;
//      Serial.println(c_f);
     




// }

//   void setup() {
//    which_loadcell(nau1, off1, c_f1);
//    Serial.println(getForce(c_f1, off1, nau1));
//    //which_loadcell(nau2, off2, c_f2);
// }



// void loop() {
 
//     //Serial.println(getForce(c_f1, off1, nau1));
//     //Serial.println(nau1.read());
    
// }



