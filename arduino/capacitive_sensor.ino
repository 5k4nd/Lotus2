#include <CapacitiveSensor.h>

/*
 * CapitiveSense for Le Lotus inspired by Library Demo Sketch from Paul Badger.
 * Uses a high value resistor e.g. 1M between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50K - 50M. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 * Bapt Abl, 2017.
 */


CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);        // 1M resistor between pins 4 & 2, pin 2 is sensor pin

void setup()                    
{
   cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
   Serial.begin(115200);
}

void loop()                    
{
    long start = millis();
    long pin2_value =  cs_4_2.capacitiveSensor(30);
    long measurement_delay = millis() - start;
    Serial.print("{'capa':");
    Serial.print(pin2_value);
    Serial.println("}");
    //Serial.print(measurement_delay);        // check on performance in milliseconds

    delay(10);
}