# Lotus2
Seconde version du Lotus, code d'une installation interactive développée en partenariat avec le Théâtre Impérial de Compiègne.

Cette version se sépare de l'interface ncurses et d'une conception rigoureuse d'un point de vue
orienté objet et ontologies, mais désastreux côté performance. Place à la programmation séquentielle !

#       #
Le Lotus
#       #

Programme réalisé dans le cadre d'un projet UTCéen en partenariat avec le Théâtre Impérial de Compiègne.
Codé en Python 2 et en Arduino, l'application finale tourne simultanément sur un Raspberry Pi et plusieurs cartes Arduino.
Le Pi traite des signaux en provenance de l'arduino, et y associe des effets lumineux (via le protocole DMX) et sonores (protocole RCA).




###################################
####### Architecture du projet
###################################

-- /        contient le code python
-- arduino/     contient le code arduino
-- data/        contient l'ensemble des fichiers utilisés par le pi, notamment la musique




####################################
######### pour le python
####################################

Lancer l'application avec
  ./main.py


n'oubliez pas :

  * de lancer ce programme en root si vous êtes sous Linux
  * de configurer les ports et bauds des arduinos dans les premières lignes du fichier main.py



pour lancer l'application dans un environnement virtuel :
  virtualenv env

se placer dans cet environnement :
  source env/bin/activate

installer les modules python :
  pip install -r requirements.txt

pour sortir du virtualenv :
  deactivate
