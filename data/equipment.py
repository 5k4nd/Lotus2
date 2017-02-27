# -*- coding: utf-8 -*-

"""

DÉFINITION DU MATÉRIEL UTILISÉ (LAMPES, SPOTS, ETC.)

les PAR-LED sont disposés dans le sens des aiguilles d'une montre dans
l'ordre 1, 2, 3, 4, le 1 étant tout de suite à gauche quand on rentre
dans la salle.


"""
class PARLED():
    def __init__(self, address):
        self.r = address + 1
        self.g = address + 2
        self.b = address + 3


class RGB():
    def __init__(self, address):
        self.r = address
        self.g = address + 1
        self.b = address + 2
        self.all = [self.r, self.g, self.b]

    def __repr__(self):
        return int(str(self.r))


PARLED_1 = PARLED(address=1)
2
3
4

PARLED_2 = PARLED(address=6)
7
8
9


PARLED_3 = PARLED(address=11)
12
13
14

PARLED_4 = PARLED(address=16)
17
18
19


BANDEAU_LED = RGB(address=21)

PAR_1000 = 24

