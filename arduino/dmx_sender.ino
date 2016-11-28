 //infos matos: par a led rgb 64 https://www.woodbrass.com/par-a-led-eagletone-parled-64-rgb-p99694.html
  
  // cette partie de code permet de controler la couleur de la light, l'arduino sert alors juste de passerelle entre le PC (python) et la light (DMX)
  //le code reçu est de la forme DRRR,GGG,BBB
  
  // librairie pour gérer le DMX
  #include <DmxSimple.h>
  
  
  void setup() {
    // on n'utilise qu'une pin pour la sortie, par laquelle transite toute la trame
    DmxSimple.usePin(3);
  
    // nombre de channels disponibles sur notre light
    DmxSimple.maxChannel(5);
    // pour écrire dans chaque channel on utilisera write
    
    Serial.begin(115200);
  }
  
 
  
  
  /*le code reçu est de la forme DRRR,GGG,BBB
  avec D caractère,
  RRR, GGG et BBB intensité du rouge, vert et bleu (entre 0 et 255)
  si ces valeurs sont inférieures à 0, elles seront mises à 0,
  si elles sont supérieures à 255 elles seront mises à 255.*/
  int red;
  int green;
  int blue;
  
  
  void loop() {
    

    // récupérer la couleur envoyée par le python sous la forme RRRGGGBBB
    if (Serial.available() && Serial.read() == 'D')
    {
      red = Serial.parseInt();
      red = constrain(red, 0, 255);
      green =  Serial.parseInt();
      green = constrain(green, 0, 255);
      blue =  Serial.parseInt(); 
      blue = constrain(blue, 0, 255);
    }
     
  
    Serial.println(red, DEC);
    Serial.println(green, DEC);
    Serial.println(blue, DEC);
    
    //  valeurs entre 0 (éteint) et 255 (allumé)
    DmxSimple.write(1, 0);// mode (inutilisé)
    DmxSimple.write(2, red); // rouge
    DmxSimple.write(3, green); // vert
    DmxSimple.write(4, blue); // bleu
    DmxSimple.write(5, 0); // vitesse (inutilisé)
    delay(1);
    
  }
  
