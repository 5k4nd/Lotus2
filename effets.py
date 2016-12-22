#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dmx_functions import DMX
from audio_functions import *
import gevent
#from gevent import getcurrent
from gevent.pool import Group

class Effets():
    """
        dans cette classe se trouvent tous les effets.
        généralement un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son
    """
    def __init__(self, ard_dmx, ard_sensors):
        self.dmx = DMX()
        self.ard_dmx = ard_dmx
        self.ard_sensors = ard_sensors





    def sequence(self):
        print('START SEQUENCE')
        audio_sequence(2)
        dmx = self.dmx
        dmx.zero()
        sleep(2)
        SS = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.02)
        G = []
        G.extend( dmx.multi(0, dmx.fade, [4, 9], 0.2, 0, 255, 6) ) #bleu vers blanc
        G.extend( dmx.multi(0.5, dmx.fade, [2, 3, 7, 8], 1, 0, 255, 4) )#bleu vers blanc
        G.extend( dmx.multi(0, dmx.fade_up_down, [12, 17], 0.8, 0, 255, 8))
        G.extend( dmx.multi(0, dmx.fade_up_down, [14, 19], 0.8, 0, 255, 8)) #fade up down rose
        G.extend( dmx.multi_boucle(1.2, 19, dmx.fade_up_down, [2,3,4,7,8,9], 0.2, 0, 255, 8)) #fade up 0.2s phase 1
        g = gevent.spawn_later(1.5, dmx.interruption,[2,3,4], 2)
        G.extend( dmx.multi(1.6, dmx.fade, [2], 0.2, 0, 255, 6, 1) )
        g = gevent.spawn_later(4, dmx.interruption,[2,3,4], 0)
        #G.extend(gevent.spawn_later(2, dmx.interruption, [2,3,4], 0))
        G.extend( dmx.multi_boucle(3.1, 17, dmx.fade_up_down, [12,13,14,17,18,19], 0.2, 0, 255, 8)) #fade up 0.2s phase 2
        G.extend( dmx.multi(5, dmx.fade, [2,3,4,7,8,9], 3, 255, 0, 2)) #fade down
        G.extend( dmx.multi(6.5, dmx.fade, [12,13,14,17,18,19], 1.5, 255, 0, 2)) #fade down
        G.extend( dmx.multi_boucle(9.5, 3, dmx.fade_up_down, [2,4], 3, 50, 255, 4))
        G.extend( dmx.multi_boucle(13.5, 2, dmx.fade_up_down, [7,9], 3, 50, 255, 4))
        #G.extend( gevent.spawn_later(9.5, dmx.fade, 2, 1.5, 0, 255, 4))

        #g3 = gevent.spawn_later(1, dmx.boucle, dmx.fade_up_down, 3, 8, 3, 100, 255)
        gevent.joinall(G)
        SS.kill()
        print ('fin')

    # def battement_de_coeur_1(self):
    #     dmx = self.dmx
    #     while 1:
            # distance = self.ard_sensors.data['capt1']

    def sequence_stop(self):
        audio_stop(2)
        

    def battement_de_coeur(self):
        """
        battement de coeur en fonction de la distance, comprise sur [1, 239].
        on divise par 210 pour obtenir un pas de 30cm, soit 7 niveaux en tout.
        
        La fonction appelle respectivement les fonctions de lumières (DMX) et de son (VLC)

        """
        dmx = DMX()
        distance = self.ard_sensors.data['capt1']  # remplacer par un truc pertinent !
        # distance = 9  # pour les tests

        # si jamais on a plus de 239 cm on gère pas, donc on ramène à du connu
        if distance > 239:
            distance = 239
        level = int(distance/30) + 1

        # son
        print("battement %s" % level)
        audio_battement(level=level)

        # lumière
        g1 = gevent.spawn(dmx.battement, canal=2, duree=.8, val_dep=0, val_fin=255)
        g4 = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.03)
        gevent.joinall([g1])
        g4.kill()

        # gestion des palliers
        if level==1:
            sleep(.2)
        elif level==2:
            sleep(.3)
        elif level==3:
            sleep(.4)
        elif level==4:
            sleep(.5)
        elif level==5:
            sleep(.7)
        elif level==6:
            sleep(.9)
        elif level==7:
            sleep(1.1)
        elif level==8:
            sleep(1.3)

