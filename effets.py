#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent

from gevent.pool import Group
from time import sleep, time

from dmx_functions import DMX
from audio_functions import *
from data.materiel import *



class Effets():
    """
        dans cette classe se trouvent tous les effets.
        un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son d'audio_functions

        un effet lumineux est lancée via un spaw gevent qui respecte ces conventions :

        G.extend(
            dmx.multi
            (
                0,              # delai avant demarrage
                dmx.fade,       # fonction appelée, ici pour bleu vers blanc
                [4, 9],         # sur channels
                0.2, 0, 255, 6  # ensuite c'est des parametres
            )
        )
 

    """

    def __init__(self, arduino_dmx, arduino_ultrasonics, arduino_lotus):
        self.dmx = DMX()
        self.arduino_dmx = arduino_dmx
        self.arduino_ultrasonics = arduino_ultrasonics
        self.arduino_lotus = arduino_lotus



    def sequence(self, ref_thread_events):
        """
            la séquence principale des sirènes, chronologiquement par effet lumière
            et accessoirement effets sonores
        """

        tic = time()
        audio_sequence(ref_thread_events)
        dmx = self.dmx
        dmx.zero()
        SS = gevent.spawn(dmx.send_serial, self.arduino_dmx, 0.02)
        G = []

        # cette fonction duplique dmx.fade pour les canaux 4 et 9 et les lance
        G.extend(
            dmx.multi
            (
                0,              # delai avant demarrage
                dmx.fade,       # fonction appelée, ici pour bleu vers blanc
                [4, 9],         # sur channels
                0.2, 0, 255, 6  # ensuite c'est des parametres
            )
        )

        G.extend( dmx.multi(0, dmx.fade_up_down, [12, 17], 0.8, 0, 255, 8))
        G.extend( dmx.multi(0, dmx.fade_up_down, [14, 19], 0.8, 0, 255, 8)) #fade up down rose
        G.extend( dmx.multi(0.5, dmx.fade, [2, 3, 7, 8], 1, 0, 255, 4) )#bleu vers blanc
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
        G.extend( dmx.multi(19, dmx.fade, [4], 1, 0, 255, 2))
        G.extend( dmx.multi(20, dmx.fade, [4], 0.5, 255, 0, 4))
        G.extend( dmx.multi(20.3, dmx.fade_up_down_kill, [7,9], 0.8, 50, 255, 6, 20.2))  # cette ligne était commentée... erreur ? >> investiguer
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
            if (self.arduino_lotus.must_start_sequence == True):  # tant que la séquence doit continuer
                j = gevent.spawn( dmx.fade_up_down, PAR_1000, 1, 0, 150, 6, 0)
                gevent.joinall([j])

        #g3 = gevent.spawn_later(1, dmx.boucle, dmx.fade_up_down, 3, 8, 3, 100, 255)

        sleep(2)
        SS.kill()
        print('EFFET: fin séquence sirènes')
        # print time()-tic



    def battement_de_coeur(self, dmx, ref_thread_events):
        """
            battement de coeur lorsque des visiteurs sont entrés.
            - level 1 lorsqu'ils sont loins
            - level 2 lorsqu'ils sont proches

        """


        
        duree_bat = 0.35
        level = 1

        audio_battement(level=level, ref_thread_events=ref_thread_events)

        
        g_par_1000 = gevent.spawn(dmx.constant, PAR_1000, 50)
        
        g_bandeau = gevent.spawn(dmx.constants, [BANDEAU_LED.r, BANDEAU_LED.g, BANDEAU_LED.b], [255, 0, 0])

        g_dmx = gevent.spawn(dmx.send_serial, self.arduino_dmx, 0.02)
        
        g_PARLEDs = []
        g_PARLEDs.extend( dmx.multi(0, dmx.battement, [2, 7,12 ,17], duree_bat, 0, 255, 4))


        # on attend la fin du battement MAIS on INTERROMPT le battement si le lotus est touché ! 
        while (len(gevent.joinall(g_PARLEDs, timeout=0)) != len(g_PARLEDs)):
            if (self.arduino_lotus.must_start_sequence == True):
                break


        if level==1:
            tic = time()
            while (time() - tic < 1.3) and (self.arduino_lotus.must_start_sequence == False):
                sleep(.1)

        elif level==2:
            tic = time()
            while (time() - tic < .3) and (self.arduino_lotus.must_start_sequence == False):
                sleep(.1)


        g_par_1000.kill()
        g_bandeau.kill()
        # g_bandeau_g.kill()
        # g_bandeau_b.kill()
        # dmx.valeur([2, 7, 12, 17, PAR_1000], [0,0,0,0,0])
        # dmx.blackout([2, 7, 12, 17, PAR_1000, BANDEAU_LED])
        # print("\nblackout")
        g_dmx.kill()


    def sequence_intro_caverne(self, dmx, ref_thread_events):

        audio_intro(ref_thread_events=ref_thread_events)

        g_dmx = gevent.spawn(dmx.send_serial, self.arduino_dmx, 0.03)

        g_parled_4 = gevent.spawn(dmx.constants, [PARLED_4.r, PARLED_4.g, PARLED_4.b], [10, 50, 10])

        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.r, R-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.g, G-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.b, B-100)
        # g_bandeau = []

        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.r, R-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.g, G-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.b, B-100)

        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.r, R-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.g, G-100)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.b, B-100)

        # g_bandeau.extend( dmx.multi(1, dmx.fade, [BANDEAU_LED.g], .3, 0, 30, 1))
        # gevent.joinall(g_bandeau, timeout=0)

        while not(ref_thread_events.thread_ultrasonics.visitors_detected):
            # g_bandeau.extend( dmx.multi(0, dmx.lotus_oscillations_intro, [BANDEAU_LED.r]))
            g_bandeau = gevent.spawn(dmx.lotus_oscillations_intro, BANDEAU_LED.r)
            gevent.joinall([g_bandeau])
            # while (len(gevent.joinall(g_bandeau)) != len(g_bandeau)):
            #     if ref_thread_events.thread_ultrasonics.visitors_detected:
            #         break
                


            # while (len(gevent.joinall(g_bandeau, timeout=0)) != len(g_bandeau)):
            #     if ref_thread_events.thread_ultrasonics.visitors_detected:
            #         break

        # pouet = gevent.spawn(dmx.constant, [BANDEAU_LED.r], 0)
        # gevent.joinall(pouet)
        # print("COUCOU")
        # g_bandeau.kill()
        # gg = gevent.spawn(dmx.constant, BANDEAU_LED.r, 0)
        
        audio_stop("intro")
        # g_parleds = gevent.spawn(dmx.constant, PARLED_1.r, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_1.g, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_1.b, 0)

        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.r, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.g, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_2.b, 0)
        # g_bandeau = []

        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.r, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.g, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_3.b, 0)

        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.r, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.g, 0)
        # g_parleds = gevent.spawn(dmx.constant, PARLED_4.b, 0)

        # sleep(1)
        # g_parleds.kill()
        # g_bandeau.kill()
        g_parled_4.kill()
        g_dmx.kill()


        