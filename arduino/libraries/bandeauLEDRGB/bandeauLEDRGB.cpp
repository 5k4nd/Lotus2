
#if defined(ARDUINO) && ARDUINO >= 100 // choisit la libairie selon la version du logiciel arduino
#include "Arduino.h"    // for digitalRead, digitalWrite, etc
#else
#include "WProgram.h"
#endif
#include "bandeauLEDRGB.h"




//---------------------constructeurs--------------------------------------
  bandeauLEDRGB::bandeauLEDRGB(uint8_t rouge, uint8_t vert, uint8_t bleu){
    
    active = false ;
    bandeauRGB[0] = rouge ;
    bandeauRGB[1] = bleu ;
    bandeauRGB[2] = vert ;
    pinMode(bandeauRGB[0],OUTPUT) ;
    pinMode(bandeauRGB[1],OUTPUT) ;
    pinMode(bandeauRGB[2],OUTPUT) ;
  }

  
 bandeauLEDRGB::bandeauLEDRGB(uint8_t pinrouge, uint8_t pinvert, uint8_t pinbleu, bool activation){
    
    active = activation ;
    bandeauRGB[0] = pinrouge ;
    bandeauRGB[1] = pinbleu ;
    bandeauRGB[2] = pinvert ;
    pinMode(bandeauRGB[0],OUTPUT) ;
    pinMode(bandeauRGB[1],OUTPUT) ;
    pinMode(bandeauRGB[2],OUTPUT) ;
  }
  
//------------------fonctions pour colorer les led--------------------------------------
// on crée une fonction de controle fine pour chaque couleur de led et une plus générale par bandeau pour éviter de surcharger le code
void bandeauLEDRGB::ledpwm(uint8_t pwm, Couleur coul) // reçoit valeur 0-255 et couleur à modifier (255 est la luminosité la plus faible)
{
  
  constrain(pwm,0,255) ; // on bloque la valeur pwm entre 0 et 255
  analogWrite(bandeauRGB[coul], pwm);// la fonction crée l'onde carrée de rapport pwm sur la sortie bandeau. l'onde sera modifiée au prochain appel de la fonction.
}

void bandeauLEDRGB::ledpwmRGB(uint8_t pwmRouge,uint8_t pwmBleu,uint8_t pwmVert) // reçoit les valeur pwm pour chaque couleur et le bandeau associé
{
  constrain(pwmRouge, 0, 255) ;
  constrain(pwmBleu, 0, 255) ;
  constrain(pwmVert, 0, 255) ;
  analogWrite(bandeauRGB[0], pwmRouge);
  analogWrite(bandeauRGB[1], pwmVert);
  analogWrite(bandeauRGB[2], pwmBleu);
}

bool bandeauLEDRGB::istrue(void)
{
  return active ;
}

void bandeauLEDRGB::settrue(bool valeur)
{
 active = valeur ;
}

