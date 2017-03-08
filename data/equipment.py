# -*- coding: utf-8 -*-

"""

DÉFINITION DU MATÉRIEL UTILISÉ (LAMPES, SPOTS, ETC.)

les PAR-LED sont disposés dans le sens des aiguilles d'une montre dans
l'ordre 1, 2, 3, 4, le 1 étant tout de suite à gauche quand on rentre
dans la salle.


"""
class PARLED():
    def __init__(self, address):
        if address is None:
            self.r = [
                PARLED_1.r,
                PARLED_2.r,
                PARLED_3.r,
                PARLED_4.r
            ]
            self.g = [
                PARLED_1.g,
                PARLED_2.g,
                PARLED_3.g,
                PARLED_4.g
            ]
            self.b = [
                PARLED_1.b,
                PARLED_2.b,
                PARLED_3.b,
                PARLED_4.b
            ]
            self.rgb = self.r + self.g + self.b

        else:
            self.r = address + 1
            self.g = address + 2
            self.b = address + 3
            self.rgb = [self.r, self.g, self.b]


class RGB():
    def __init__(self, address):
        self.r = address
        self.g = address + 1
        self.b = address + 2
        self.rgb = [self.r, self.g, self.b]


# récapitule les adresses actuellement utilisées. utile pour la maintenance !
equipment_adresses = [1, 6, 11, 16, 21, 24]
equipment_adresse_max = max(equipment_adresses)

PARLED_1 = PARLED(address=equipment_adresses[0])

PARLED_2 = PARLED(address=equipment_adresses[1])

PARLED_3 = PARLED(address=equipment_adresses[2])

PARLED_4 = PARLED(address=equipment_adresses[3])

PARLED_ALL = PARLED(None)

BANDEAU_LED = RGB(address=equipment_adresses[4])

PC_1000 = equipment_adresses[5]



if __name__ == '__main__':
    print(adresse_max)
