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
        dmx = self.dmx
        dmx.zero()
        sleep(2)
        SS = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.02)
        G = []
        G.extend( dmx.multi(0, dmx.fade, [4, 9], 0.2, 0, 255, 6) ) #bleu vers blanc
        G.extend( dmx.multi(0.5, dmx.fade, [2, 3, 7, 8], 1, 0, 255, 4) )#bleu vers blanc
        G.extend( dmx.multi(0, dmx.fade_up_down, [12, 17], 0.8, 0, 255, 8))
        G.extend( dmx.multi(0, dmx.fade_up_down, [14, 19], 0.8, 0, 255, 8)) #fade up down rose
        G.extend( dmx.multi_boucle(1.2, 19, dmx.fade_up_down, [2,3,4,7,8,9], 0.4, 0, 255, 8)) #fade up 0.2s phase 1
        G.extend( dmx.multi_boucle(3.1, 17, dmx.fade_up_down, [12,13,14,17,18,19], 0.4, 0, 255, 8)) #fade up 0.2s phase 2
        G.extend( dmx.multi(5, dmx.fade, [2,3,4,7,8,9], 3, 255, 0, 2)) #fade down
        G.extend( dmx.multi(6.5, dmx.fade, [12,13,14,17,18,19], 1.5, 255, 0, 2)) #fade down
        G.extend( dmx.multi_boucle(9.5, 3, dmx.fade_up_down, [2,4], 3, 100, 255, 4))
        G.extend( dmx.multi_boucle(9.5, 2, dmx.fade_up_down, [6,8], 3, 100, 255, 4))
        #g10 = gevent.spawn_later(9.5, dmx.boucle, 6, dmx.multi, dmx.fade, [2,4,7,9], 1.5, 0, 255, 4)

        #g3 = gevent.spawn_later(1, dmx.boucle, dmx.fade_up_down, 3, 8, 3, 100, 255)
        gevent.joinall(G)
        SS.kill()
        print ('fin')
    def battement_de_coeur_1(self):
        dmx = self.dmx
        while 1:
            distance = self.ard_sensors.data['capt1']

    def battement_de_coeur(self):
        # distance = self.ard_sensors.data['capt1']  # remplacer par un truc pertinent !
        distance = 220  # pour les tests
        if distance < 50:
            print("battement 1")
            # DMX.battement(self.ard_dmx, 0, 150, 8)
            audio_battement(level=1)

        elif ((distance >= 50) & (distance < 100)):
            print("battement 2")
            # DMX.battement(self.ard_dmx, 0, 150, 6)
            audio_battement(level=2)
        elif ((distance >= 100) & (distance < 200)):
            print("battement 3")
            audio_battement(level=3)
            DMX.battement(self.ard_dmx, 0, 150, 3)
        elif distance >= 200:
            print("battement 7")
            audio_battement(level=3)
            # DMX.battement(self.ard_dmx, 0, 150, 3)
