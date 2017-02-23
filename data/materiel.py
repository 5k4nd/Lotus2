# -*- coding: utf-8 -*-

"""

DÉFINITION DU MATÉRIEL UTILISÉ (LAMPES, SPOTS, ETC.)

les PAR-LED sont disposés dans le sens des aiguilles d'une montre dans
l'ordre 1, 2, 3, 4, le 1 étant tout de suite à gauche quand on rentre
dans la salle.


"""
class PARLED():
    def __init__(self, adresse):
        self.r = adresse + 1
        self.g = adresse + 2
        self.b = adresse + 3

class BANDEAU_LED():
    def __init__(self, adresse):
        self.r = adresse
        self.g = adresse + 1
        self.b = adresse + 2


PARLED_1 = PARLED(adresse=1)
PARLED_2 = PARLED(adresse=6)
PARLED_3 = PARLED(adresse=11)
PARLED_4 = PARLED(adresse=16)


BANDEAU_LED = BANDEAU_LED(adresse=21)

PAR_1000 = 24


