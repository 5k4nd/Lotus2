#ifndef PROTOCOLE_PYTHON
#define PROTOCOL_PYTHON

#if defined(ARDUINO) && ARDUINO >= 100
#include "Arduino.h"    // for digitalRead, digitalWrite, etc
#else
#include "WProgram.h"
#endif

class communicationpy
{
    uint8_t ambiance ;
  public:
    communicationpy():ambiance(0) {};
    int getambiance() const { return this->ambiance ;} ;
    void setambiance(uint8_t amb) { this->ambiance = amb ;};
    int PCToArd() ;
    void ArdToPC(String nomVar, uint8_t valVar ) ;
    void CaptToPC(String captname, uint8_t captvalue);//, uint8_t capteur2, uint8_t capteur3, uint8_t capteur4, uint8_t lotus) ;
    
} ;


#endif