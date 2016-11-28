
//#ifndef CAPT_ULTR_SON
#define CAPT_ULTR_SON
#include <NewPing.h>


// capt1
#define CAPT1_TRIGGER_PIN 11   // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define CAPT1_ECHO_PIN 12  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE  200

NewPing sonar1(CAPT1_TRIGGER_PIN,CAPT1_ECHO_PIN, MAX_DISTANCE);

unsigned int capt1 = MAX_DISTANCE ;


void mesure_ultrason()
{
  capt1 = sonar1.ping_cm() ;
  /* 
  capt2 = sonar2.ping_cm() ;
  capt3 = sonar3.ping_cm() ;
  capt4 = sonar4.ping_cm() ;
  */
}

void setup() {
  Serial.begin(115200);
}

void loop() {
  mesure_ultrason();
  Serial.print("{'") ;
  Serial.print("capt1':") ;
  Serial.print(capt1) ;
  Serial.println("}") ;
  delay(100);
}
