//----------------------------------------librairies--------------------------------------

#include "ambiances.h"

/*******************************communicationpy********************************************/
#include <communicationpy.h>


/******************************************************************************************/
/*******************************variables globales*****************************************/


//variables pour gerer la temporisation
unsigned int delais = 0 ;
unsigned int temps ; 

int ambiance = 0 ; //chaque valeur de la variable correspond à une ambiance
byte increment = 0 ; // cette variable pernet de faire une routine par rapport au temps
byte test_inc[] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30} ;
//variables des mesures de couleur à envoyer
float valrouge ;
float valbleu ;
float valvert ;
/**********************************************************************************************/
/******************************************capteur ultrason*******************************************
 * les capteurs à ultrasons sont alimentés en 5V
 */
#ifndef CAPT_ULTR_SON
#define CAPT_ULTR_SON
#include <NewPing.h>

// capt1
#define CAPT1_TRIGGER_PIN 22   // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define CAPT1_ECHO_PIN 24  // Arduino pin tied to echo pin on the ultrasonic sensor.

// capt2
#define CAPT2_TRIGGER_PIN 26 
#define CAPT2_ECHO_PIN 28 

// capt3
#define CAPT3_TRIGGER_PIN 30 
#define CAPT3_ECHO_PIN 32 

// capt4
#define CAPT4_TRIGGER_PIN 34 
#define CAPT4_ECHO_PIN 36 

#define MAX_DISTANCE  200 // Distance maximum de detection souhaitée en cm. distance max capteur 400-500cm



//-------------------------------------initialisation des capteurs-----------------------------------

NewPing sonar1(CAPT1_TRIGGER_PIN,CAPT1_ECHO_PIN, MAX_DISTANCE); // configuration du capteur.
NewPing sonar2(CAPT2_TRIGGER_PIN,CAPT2_ECHO_PIN, MAX_DISTANCE);
NewPing sonar3(CAPT3_TRIGGER_PIN,CAPT3_ECHO_PIN, MAX_DISTANCE);
NewPing sonar4(CAPT4_TRIGGER_PIN,CAPT4_ECHO_PIN, MAX_DISTANCE);

//-------------------------------------variables globales des capteurs ultrason------------------------------------------
unsigned int capt1 = MAX_DISTANCE ;
unsigned int capt2 = MAX_DISTANCE ;
unsigned int capt3 = MAX_DISTANCE ;
unsigned int capt4 = MAX_DISTANCE ;

//-----------------------fonction pour prendre les mesures de chaque capteur-----------------
// les fonctions sont directement implementées dans la librairie
void mesure_ultrason()
{
  capt1 = sonar1.ping_cm() ; // renvoie la distance en cm
  /* 
  capt2 = sonar2.ping_cm() ;
  capt3 = sonar3.ping_cm() ;
  capt4 = sonar4.ping_cm() ;
  */
}

#endif
/******************************************************************************************************/
/******************************************BANDEAUX****************************************************/
/* La luminosité des led varie en fonction de la tension entre l'entrée et la sortie.
 * L'entrée est réglée sur 12V.
 * La tension sur les sorties(chaque couleur de led) est commandée par l'arduino aux moyen d'une tension gérée par modulations d'impulsions (PWM)
 * la tension des led est la différence entre le 12V et la sortie de l'arduino [ ex : alim 12V / arduino 3V ==> 9V ]
 * l'arduino ne pouvant sortir que du 5V et une petite intensité, on utilise des transistors pour faire un circuit de puissance. 
 * 
 * -----------------------------------------PWM--------------------------------------------
 * le PWM crée une onde carrée dont dont on peut choisir le rapport entre le temps haut et le temps bas. Celui-ci est codé sur un octet. Ainsi, 
 * une valeur de 255 enverra un signal continu à 1(5V), une valeur de 0 un signal continu à 0 (0V) et un signal à 127 donne une onde carrée de rapport 0.5 (2.5V)  
 * 
 * 
 *-----------------------------------------Amplification--------------------------------------- 
 * 
 * le bandeau est alimenté en 12V et peux tirer plusieurs amperes, il faut donc mettre des transistors pour faire un circuit de puissance. 
 * Avec le transistor coté non métallique, 
 * brancher le pin de droite sur une résistance de 10KΩ relié à l'arduino
 *          le pin central sur le bandeau
 *          le pin de gauche sur la masse ( commune entre l'alim 12V et l'arduino )
 *
 * 
 * 0   ==> __________________________________________ ==> 0V    ==> amplification ==> 0V
 *          _     _     _     _     _     _     _
 * 63  ==> | |___| |___| |___| |___| |___| |___| |___ ==> 1.25V ==> amplification ==> 3V
 *          __    __    __    __    __    __    __
 * 127 ==> |  |__|  |__|  |__|  |__|  |__|  |__|  |__ ==> 2.5V  ==> amplification ==> 6V
 *          ___   ___   ___   ___   ___   ___   ___
 * 191 ==> |   |_|   |_|   |_|   |_|   |_|   |_|   |_ ==> 3.75V ==> amplification ==> 9V
 *          ________________________________________
 * 255 ==> |                                        | ==> 5V    ==> amplification ==> 12V
 * 
 * 
 */
#include <bandeauLEDRGB.h>
//-------------------------------on crée tous les bandeaux de led----------------------------
// prototypes constructeur : nombandeau(unsigned int pinrouge,unsigned int pinvert,unsigned int pinbleu, bool activé ?[(optionnel) false par défaut] )

bandeauLEDRGB bandeau_pilier_1(5,6,3) ;
/* 
bandeauLEDRGB bandeau_pilier_2(3,5,6) ;
bandeauLEDRGB bandeau_pilier_3(3,5,6) ;

bandeauLEDRGB bandeau_pf_ext_1(3,5,6) ; //plateforme
bandeauLEDRGB bandeau_pf_ext_2(3,5,6) ;
bandeauLEDRGB bandeau_pf_ext_3(3,5,6) ;
bandeauLEDRGB bandeau_pf_ext_4(3,5,6) ;

bandeauLEDRGB bandeau_pf_int_1(3,5,6) ;
bandeauLEDRGB bandeau_pf_int_2(3,5,6) ;
bandeauLEDRGB bandeau_pf_int_3(3,5,6) ;
bandeauLEDRGB bandeau_pf_int_4(3,5,6) ;

bandeauLEDRGB bandeau_lotus_1(3,5,6) ;
bandeauLEDRGB bandeau_lotus_2(3,5,6) ;
bandeauLEDRGB bandeau_lotus_3(3,5,6) ;
bandeauLEDRGB bandeau_lotus_4(3,5,6) ;
*/

/*
 * ces variables servent à activer des routines qui vont se rajouter aux ambiances en fonction des 
 * demandes de l'ordinateur comme faire briller les led avec la musique. 
 */

/*******************************************************************************************************/
/*******************************************capteur capacitif*******************************************/
/*-------------------------------principe----------------------------------------------------
 * le capteur capacitif calcule le temps de charge du systeme assimilé à un condensateur de très faible capacitée
 * celui-ci est modifié quand on touche le capteur, ce qui crée un deuxième condensateur et donc un effet de résonnance. 
 * le système aura donc un temps de chargement de 1 si on ne touche pas le capteur mais pourra dépasser 1000 dès lors qu'il sera touché
 * 
 * -----------------------------branchement--------------------------------------------------
 * connecter une résistance de 1MΩ entre deux pins de l'arduino, le pin d'entrée et le pin de sortie. 
 * connecter ensuite le capteur métallique sur le pin de sortie sans lui attribuer de masse.
 */

#ifndef CAPT_CAPACITIF
#define CAPT_CAPACITIF

#include <CapacitiveSensor.h>

#define TPS_DETECTION 100 //le temps de detection est à étalonner en fonction du capteur et de la résistance. pour ça, veuillez utiliser le code de démo fourni avec la librairie.

//---------------------------------définitions des pins des capteurs--------------------------------------
// on peut prendre sans aucun problème une seule alimentation pour tous les capteurs.
CapacitiveSensor petale1 = CapacitiveSensor(31,33) ; // résistance de 1MΩ entre pin 31(alim) et 33(sortie)
CapacitiveSensor petale2 = CapacitiveSensor(31,35) ; // résistance de 1MΩ entre pin 31 et 35
CapacitiveSensor petale3 = CapacitiveSensor(31,37) ; // résistance de 1MΩ entre pin 31 et 37
CapacitiveSensor petale4 = CapacitiveSensor(31,39) ; // résistance de 1MΩ entre pin 31 et 39

//----------------variables globales capteurs---------------------------------

unsigned int lotus = 0 ; 
/* 
 * 0 ==> aucun pétale 
 * 1 ==> petale1 activé
 * 2 ==> petale2 activé
 * 3 ==> petale1 ET petale2 activés
 * 4 ==> petale3 activé
 * 8 ==> petale4 activé...
 */



//
int mesure_tactile() 
{
  
  int lotus = petale1.capacitiveSensor(30)>TPS_DETECTION ;

  return lotus ;
}
#endif
/******************************************************************************************************/


communicationpy command = communicationpy() ;
unsigned long truc = 0 ;
void setup()
{

  Serial.begin(115200);// début de la communication avec l'ordinateur avec une vitesse de 115200 (à synchroniser avec l'ordinateur)
  /*
  petale1.set_CS_AutocaL_Millis(0xFFFFFFFF) ; // initialisation du capteur capacitif du lotus
  temps = millis() ;
  */
}


/**********************************problématique du temps réel multitache en monoprocessus********************************
 * le programme devant faire un certain nombre d'action en simultané( allumage des led, prise de mesure des capteurs, dialogue avec l'ordinateur)
 * on ne peut utiliser la fonction delay pour gerer le temps d'allumage des leds, celle-ci bloqurais le programme.
 * 
 * On utilise donc une alternative à cette fonction en créant une variable qui fera tourner un certain nombre de fois la boucle principale pour "attendre"
 * On utilise par ailleurs la fonction serialEvent, déjà implémentées dans le langage arduino qui s'éxecute entre chaque boucle loop. 
 * On va lui déleguer les prise de mesures et communication pour ne mettre que la gestion des led dans la boucle principale. 
 * 
 * 
 * **********************************************principe du programme des leds********************************************
 * la boucle principale est un choix entre les différentes ambiance que l'on aura codé au préalable.
 * lors d'une temporisation, elle s'execute "à vide" en lieu et place de l'instruction delay pour rester à l'écoute des autre processus.
 * 
 */



void loop() {
  bandeau_pilier_1.ledpwm(int(254),Couleur::rouge) ;
  bandeau_pilier_1.ledpwm(int(250),Couleur::vert) ;
  bandeau_pilier_1.ledpwm(int(0),Couleur::bleu) ;
  char test[] = "coucou";
  Serial.println(test);

  /*
  if (temps+delais>millis())
  {
    switch(ambiance)
    {
// ce programme fait fluctuer la couleur des bandeaux led en fonction du temps. 
// l'intensité globale est fonction de la distance des gens avec le capteur ultrason.

      case 0 ://avant d'avoir été touché une première fois

       
        increment++ ;
        if (increment == 30) increment = 0 ;
        bandeau_pilier_1.ledpwm(int(test_inc[increment]+capt1),Couleur::rouge) ;
        bandeau_pilier_1.ledpwm(int(test_inc[increment]+capt1),Couleur::vert) ;
        bandeau_pilier_1.ledpwm(int(test_inc[increment]+capt1),Couleur::bleu) ;
        
        delais = 50 ; 
        break ;
        
// Scène de combat :
// dans le lotus deux couleurs s'affrontent.
// les deux couleurs sont bleu et rouge
// on met un bandeau de chaque coté à la couleur voulu et les deux autres vont 
// tour à tour changer de couleur.
// les bandeaux du bas vont gagne en intensité en fonction du bruit

      case 2 :
         
        valrouge = (sin(increment*2*PI/255)+1)*capt1+capt2 ;      // on prend une fonction périodique entre 0 et 2 qu'on multiplie avec la distance du capteur principal.
        valbleu = (sin((increment+123)*2*PI/255)+1)*capt1+capt3 ;  // cette fonction va faire fluctuer les couleurs rouges et bleu sur les bandeaux intermédiaires.
        bandeau_pilier_1.ledpwm(int(valrouge),Couleur::rouge) ;
        bandeau_pilier_1.ledpwm(int(valrouge),Couleur::bleu) ;
        delais = 50 ;
        break ;

    }
  
  temps = millis() ;
  }
  
  int machin = millis() ;
  int temp = ambiance ;
  ambiance = command.PCToArd() ;
  
*/
  mesure_ultrason() ;
  command.CaptToPC(capt1);//, capt2, capt3, capt4, int(mesure_tactile())) ;
  delay(1000);
  //Serial.println(millis()-truc) ;
  //Serial.println(millis()-machin) ;
  //truc = millis() ;

}
/*

void serialEvent() {
  ambiance = command.PCToArd() ;
  mesure_ultrason() ;
  mesure_tactile() ;
  command.CaptToPC(capt1, capt2, capt3, capt4, lotus) ;
  
}*/
