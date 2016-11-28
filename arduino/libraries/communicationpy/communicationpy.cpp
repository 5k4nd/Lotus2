#include "communicationpy.h"


 void communicationpy::ArdToPC(String nomVar, uint8_t valVar )
{
  Serial.print("{'") ;
  Serial.print(nomVar) ;
  Serial.print("var':") ;
  Serial.print(valVar) ;
  Serial.println("}") ;
}


void communicationpy::CaptToPC(String captname, uint8_t captvalue)//, uint8_t capteur2, uint8_t capteur3, uint8_t capteur4, uint8_t lotus)
{
  this->ArdToPC(captname, captvalue) ;
  /*
  this->ArdToPC("capteur2",capteur2) ;
  this->ArdToPC("capteur3",capteur3) ;
  this->ArdToPC("capteur4",capteur4) ;
  this->ArdToPC("lotus",int(lotus)) ;
  */
}

/*
int communicationpy::PCToArd()
{ 
    if (Serial.available() > 0)
    {
      char var = Serial.read(); // a tester pour voir si ambiance.
      this->setambiance(Serial.parseInt());
      this->ArdToPC("ambiance", ambiance);
      return this->getambiance();
    }
    return this->getambiance() ;
}
*/
int communicationpy::PCToArd()
{ 
    if (Serial.available() > 0)
    {
      char var = Serial.read();
      if (var == 'A')
      {
        int tmp = 42; // c'est une ambiance
        this->setambiance(Serial.parseInt());
        this->ArdToPC("ambiance", ambiance);
        return this->getambiance();
      }
      if (var == 'D')
      {
        // c'est du DMX
      }
    }
}