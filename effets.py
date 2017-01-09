#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dmx_functions import DMX
from audio_functions import *
import gevent
import time
#from gevent import getcurrent
from gevent.pool import Group

class Effets():
    """
        dans cette classe se trouvent tous les effets.
        généralement un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son
    """
    def __init__(self, ard_dmx, ard_sensors, ard_capacitor):
        self.dmx = DMX()
        self.ard_dmx = ard_dmx
        self.ard_sensors = ard_sensors
        self.ard_capacitor = ard_capacitor





    def sequence(self, ref_thread_outputs_arduino):
        print('START SEQUENCE')
        tic = time.time()
        audio_sequence(2, ref_thread_outputs_arduino)
        dmx = self.dmx
        dmx.zero()
        SS = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.02)
        G = []
        G.extend( dmx.multi(0, dmx.fade, [4, 9], 0.2, 0, 255, 6) ) #bleu vers blanc
        G.extend( dmx.multi(0.5, dmx.fade, [2, 3, 7, 8], 1, 0, 255, 4) )#bleu vers blanc
        G.extend( dmx.multi(0, dmx.fade_up_down, [12, 17], 0.8, 0, 255, 8))
        G.extend( dmx.multi(0, dmx.fade_up_down, [14, 19], 0.8, 0, 255, 8)) #fade up down rose
        G.extend( dmx.multi(1.2,  dmx.fade_up_down_kill, [2,3,4,7,8,9], 0.2, 0, 255, 8, 3.8)) #fade up 0.2s phase 1

        G.extend( dmx.multi(3, dmx.fade_up_down_kill, [12,13,14,17,18,19], 0.3, 0, 255, 8, 2)) #fade up 0.2s phase 2
        G.extend( dmx.multi(5, dmx.fade, [2,3,4,7,8,9], 2, 255, 0, 2)) #fade down
        G.extend( dmx.multi(5, dmx.fade, [12,13,14,17,18,19], 2, 255, 0, 2)) #fade down
        G.extend( dmx.multi(9.2, dmx.fade, [2,4], 0.3, 0, 50, 4))
        G.extend( dmx.multi_boucle(9.5, 3, dmx.fade_up_down, [2,4], 2.9, 50, 255, 4))
        G.extend( dmx.multi(19, dmx.fade, [2,4], 0.2, 50, 0, 4))
        G.extend( dmx.multi(13.2, dmx.fade, [7,9], 0.3, 0, 50, 4))
        G.extend( dmx.multi_boucle(13.5, 2, dmx.fade_up_down, [7,9], 2, 50, 255, 4))
        G.extend( dmx.multi(18, dmx.fade, [7,9], 1, 50, 0, 2))

        #page 3
        #G.extend( dmx.multi(20.3, dmx.fade_up_down_kill, [7,9], 0.8, 50, 255, 6, 20.2))
        G.extend( dmx.multi(19, dmx.fade, [4], 1, 0, 255, 2))
        G.extend( dmx.multi(20, dmx.fade, [4], 0.5, 255, 0, 4))
        G.extend( dmx.multi(20.5, dmx.fade, [9], 1, 0, 255, 2))
        G.extend( dmx.multi(21.5, dmx.fade, [9], 0.5, 255, 0, 4))
        G.extend( dmx.multi(22, dmx.fade, [14], 1, 0, 255, 2))
        G.extend( dmx.multi(23, dmx.fade, [14], 0.5, 255, 0, 4))
        G.extend( dmx.multi(23.5, dmx.fade, [19], 1, 0, 255, 2))
        G.extend( dmx.multi(24.5, dmx.fade, [19], 0.5, 255, 0, 4))
        G.extend( dmx.multi(25, dmx.fade, [4], 1, 0, 255, 2))
        G.extend( dmx.multi(26, dmx.fade, [4], 0.5, 255, 0, 4))
        G.extend( dmx.multi(26.5, dmx.fade, [9], 1, 0, 255, 2))
        G.extend( dmx.multi(27.5, dmx.fade, [9], 0.5, 255, 0, 4))
        G.extend( dmx.multi(28, dmx.fade, [2,4,7,9,12,14,17,19], 2, 0,255, 2))
        G.extend( dmx.multi(30, dmx.fade, [2,4,7,9,12,14,17,19], 0.4, 255, 0, 2))
        G.extend( dmx.multi(30.5, dmx.fade, [2,7,12,17], 1, 0,255, 2))
        G.extend( dmx.multi(31.5, dmx.fade, [2,7,12,17], 1, 255,0, 2))
        #circle
        G.extend( dmx.effet_gouttes(32.5, 14, 0.5))
        G.extend( dmx.rire(40.4, 1, [2,3], [2,3,4]))
        G.extend( dmx.rire(41.4, 1, [7,8], [7,8,9]))
        G.extend( dmx.rire(46.5, 1, [12,13], [12,13,14]))
        G.extend( dmx.rire(50.4, 1, [17,18], [17,18,19]))
        G.extend( dmx.rire(48, 1, [2,3], [2,3,4]))
        G.extend( dmx.rire(55.5, 1, [7,8], [7,8,9]))
        G.extend( dmx.rire(52.5, 1, [12,13], [12,13,14]))
        G.extend( dmx.rire(53.5, 1, [17,18], [17,18,19]))
        G.extend( dmx.rire(51.4, 1, [2,3], [2,3,4]))
        G.extend( dmx.rire(56, 1, [7,8], [7,8,9]))
        G.extend( dmx.multi(60.5, dmx.fade_up_down, [2,4], 0.5, 20, 255, 4))
        G.extend( dmx.multi(61, dmx.fade_up_down, [7,9], 0.5, 20, 255, 4))

        #1er cri
        G.append( gevent.spawn_later(61.7, dmx.strobe, [2,3,4,7,8,9,12,13,14,17,18,19], 1, 100, 255, 15))
        G.extend( dmx.multi(62.8, dmx.fade, [2,3,4,7,8,9,12,13,14,17,18,19], 0.2, 0,255, 2))
        G.extend( dmx.multi(63, dmx.fade, [2,3,4,7,8,9,12,13,14,17,18,19], 2, 255, 0, 2))
        G.append( gevent.spawn_later(65.1, dmx.strobe, [2,3,4,7,8,9,12,13,14,17,18,19], 2, 100, 255, 15))

        G.extend( dmx.multi(67.5,  dmx.fade_up_down_kill, [2,4,7,9,12,14,17,19], 1, 20, 255, 4, 4.7))

        G.extend( dmx.effet_grad(72.5, 23, 1.5, 0.3 ))

        G.extend( dmx.inter_fade(78, 7, 0.2, [2], [2,3,4]))
        G.extend( dmx.inter_fade(78, 7, 0.3, [7], [7,8,9]))
        G.extend( dmx.inter_fade(78, 6, 0.4, [12], [12,13,14]))
        G.extend( dmx.inter_fade(78, 6, 0.5, [17], [17,18,19]))


        G.extend( dmx.multi(96, dmx.fade, [12,13,14,17,18,19], 0.5, 255, 0, 2)) #fade down

        G.extend( dmx.multi(95.5,  dmx.fade_up_down_kill, [2,3,4,7,8,9], 0.2, 0, 255, 8, 2.9)) #fade up 0.2s phase 1

        G.extend( dmx.multi(97, dmx.fade_up_down_kill, [12,13,14,17,18,19], 0.3, 0, 255, 8, 1.5)) #fade up 0.2s phase 2
        G.extend( dmx.multi(98.5, dmx.fade, [2,3,4,7,8,9], 2, 255, 0, 2)) #fade down
        G.extend( dmx.multi(98.5, dmx.fade, [12,13,14,17,18,19], 2, 255, 0, 2)) #fade down

        while (len(gevent.joinall(G, timeout=0)) != len(G)) :
            if (self.ard_capacitor.must_start_sequence == True):
                j = gevent.spawn( dmx.fade_up_down, 21, 1, 0, 150, 6, 0)
                gevent.joinall([j])

        #g3 = gevent.spawn_later(1, dmx.boucle, dmx.fade_up_down, 3, 8, 3, 100, 255)
        # print("fin")
        #gevent.joinall(G)
        sleep(2)
        SS.kill()
        # print ('fin')
        # print time.time()-tic

    # def battement_de_coeur_1(self):
    #     dmx = self.dmx
    #     while 1:
            # distance = self.ard_sensors.data['capt1']

    # def sequence_stop(self):
    #     audio_stop(2)


    def battement_de_coeur(self, dmx, ref_thread_outputs_arduino):
        """
        battement de coeur en fonction de la distance, comprise sur [1, 239].
        on divise par 210 pour obtenir un pas de 30cm, soit 7 niveaux en tout.

        La fonction appelle respectivement les fonctions de lumières (DMX) et de son (VLC)

        """

        duree_bat = 0.5
        #distance = self.ard_sensors.data['capt1']  # remplacer par un truc pertinent !
        distance = 150  # pour les tests

        # si jamais on a plus de 239 cm on gère pas, donc on ramène à du connu
        if distance > 239:
            distance = 239
        level = int(distance/30) + 1
        level =8
        # son
        print("battement %s" % level)
        audio_battement(level=level, ref_thread_outputs_arduino=ref_thread_outputs_arduino)

        # lumière
        #g1 = gevent.spawn(dmx.battement, canal=2, duree=.8, val_dep=0, val_fin=255)
        #g4 = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.03)
        #gevent.joinall([g1])
        #g4.kill()
        G=[]
        F = gevent.spawn(dmx.constant, 21, 50)
        SS = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.02)
        G.extend( dmx.multi(0, dmx.battement, [2, 7,12 ,17], duree_bat, 0, 255, 4))
        fin = 0
        while (len(gevent.joinall(G, timeout=0)) != len(G)) and (fin == 0):
            #print(len( gevent.joinall(G, timeout=0)))
            if (self.ard_capacitor.must_start_sequence == True):
                # print("boucle 1:")
                # print(self.ard_capacitor.must_start_sequence)
                fin = 1

        #gevent.joinall(G)
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
            tic = time.time()
            while (time.time() - tic < 1.3) and (self.ard_capacitor.must_start_sequence == False):
                foo = 42
                # print("boucle 2:")
                # print(self.ard_capacitor.must_start_sequence)


        F.kill()
        dmx.valeur([2,7,12,17,21], [0,0,0,0,0])
        SS.kill()
