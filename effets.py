#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent

from gevent.pool import Group
from time import sleep, time

from dmx_functions import DMX
from audio_functions import *
from data.materiel import *



"""

ToDo : détruire la classe DMX et faire un import *

- supprimer la méthode fade_up_down_kill, a priori c'est un patch


"""




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

        audio_sequence(ref_thread_events)

        tic = time()
        TEMPS_INITIAL = 0


        dmx = self.dmx
        dmx.blackout()
        
        # se charge d'envoyer les trames en continu, jusqu'à ce qu'on le kill à la fin de cette méthode
        g_dmx = gevent.spawn(dmx.send_serial, self.arduino_dmx, 0.02)
        
        parleds = []

        ## INTRO
        # bleu vers blanc
        parleds += dmx.multi(TEMPS_INITIAL+0,  dmx.fade_up, [PARLED_1.b, PARLED_2.b], 0.2, 0, 255, 6)
        parleds += dmx.multi(TEMPS_INITIAL+0.5,dmx.fade_up, [PARLED_1.r, PARLED_1.g, PARLED_2.r, PARLED_2.g], 1, 0, 255, 4)
        
        #fade up down rose
        parleds += dmx.multi(TEMPS_INITIAL+0,  dmx.fade_up_down_NEW, [PARLED_3.r, PARLED_4.r], 0.8, 0, 255, 8)
        parleds += dmx.multi(TEMPS_INITIAL+0,  dmx.fade_up_down_NEW, [PARLED_3.b, PARLED_4.b], 0.8, 0, 255, 8)
        
        # #fade up 0.2s phase 1
        parleds += dmx.multi(TEMPS_INITIAL+1.2,dmx.fade_up_down_kill, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r, PARLED_2.g, PARLED_2.b], 0.2, 0, 255, 8, 3.8)
        parleds += dmx.multi(TEMPS_INITIAL+3,  dmx.fade_up_down_kill, [PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 0.3, 0, 255, 8, 2) #fade up 0.2s phase 2
        parleds += dmx.multi(TEMPS_INITIAL+5,  dmx.fade_down, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r, PARLED_2.g, PARLED_2.b], 2, 255, 0, 2)
        parleds += dmx.multi(TEMPS_INITIAL+5,  dmx.fade_down, [PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 2, 255, 0, 2)


        ## premières paroles (VIOLET)
        parleds += dmx.multi(TEMPS_INITIAL+9.2,dmx.fade_up, [PARLED_1.r,PARLED_1.b], 0.3, 0, 50, 4)
        parleds += dmx.multi_boucle(TEMPS_INITIAL+9.5, 3, dmx.fade_up_down_NEW, [PARLED_1.r, PARLED_1.b], 2.9, 50, 255, 4)
        parleds += dmx.multi(TEMPS_INITIAL+19, dmx.fade_down, [PARLED_1.r, PARLED_1.b], 0.2, 50, 0, 4)

        parleds += dmx.multi(TEMPS_INITIAL+13.2, dmx.fade_up, [PARLED_2.r, PARLED_2.b], 0.3, 0, 50, 4)
        parleds += dmx.multi(TEMPS_INITIAL+13.5, dmx.fade_up_down_NEW, [PARLED_2.r, PARLED_2.b], 2, 50, 255, 7)
        parleds += dmx.multi(TEMPS_INITIAL+18, dmx.fade_down, [PARLED_2.r, PARLED_2.b], 1, 50, 0, 2)


        ## HARPE - suite des paroles (BLEU)
        # parleds.extend( dmx.multi(20.3, dmx.fade_up_down_kill, [PARLED_2.r,9], 0.8, 50, 255, 6, 20.2))  # cette ligne était commentée... erreur ? >> investiguer
        parleds += dmx.multi(TEMPS_INITIAL+19, dmx.fade_up, [PARLED_1.b], 1, 0, 255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+20, dmx.fade_down, [PARLED_1.b], 0.5, 255, 0, 5)
        parleds += dmx.multi(TEMPS_INITIAL+20.5, dmx.fade_up, [PARLED_2.b], 1, 0, 255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+21.5, dmx.fade_down, [PARLED_2.b], 0.5, 255, 0, 4)
        parleds += dmx.multi(TEMPS_INITIAL+22, dmx.fade_up, [PARLED_3.b], 1, 0, 255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+23, dmx.fade_down, [PARLED_3.b], 0.5, 255, 0, 4)
        parleds += dmx.multi(TEMPS_INITIAL+23.5, dmx.fade_up, [PARLED_4.b], 1, 0, 255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+24.5, dmx.fade_down, [PARLED_4.b], 0.5, 255, 0, 4)
        parleds += dmx.multi(TEMPS_INITIAL+25, dmx.fade_up, [PARLED_1.b], 1, 0, 255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+26, dmx.fade_down, [PARLED_1.b], 0.5, 255, 0, 4)
        parleds += dmx.multi(TEMPS_INITIAL+26.5, dmx.fade_up, [PARLED_2.b], 1, 0, 255, 4)
        parleds += dmx.multi(TEMPS_INITIAL+27.5, dmx.fade_down, [PARLED_2.b], 0.5, 255, 0, 2)
        parleds.append( gevent.spawn_later(TEMPS_INITIAL+31, dmx.constants, [PARLED_2.b], [0]) )  # forcer à zéro (chais pas pourquoi, ça redescend pas sinon...)

        ## fade up down rose
        parleds += dmx.multi(TEMPS_INITIAL+28, dmx.fade_up, [PARLED_1.r, PARLED_1.b, PARLED_2.r, PARLED_2.b, PARLED_3.r, PARLED_3.b, PARLED_4.r, PARLED_4.b], 2, 0,255, 4)
        parleds += dmx.multi(TEMPS_INITIAL+30, dmx.fade_down, [PARLED_1.r, PARLED_1.b, PARLED_2.r, PARLED_2.b, PARLED_3.r, PARLED_3.b, PARLED_4.r, PARLED_4.b], 0.4, 255, 0, 4)

        ## éclat rouge
        parleds += dmx.multi(TEMPS_INITIAL+30.5, dmx.fade_up, [PARLED_1.r,  PARLED_2.r, PARLED_3.r,PARLED_4.r], 1, 0,255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+31.5, dmx.fade_down, [PARLED_1.r,  PARLED_2.r, PARLED_3.r,PARLED_4.r], 1, 255,0, 2)


        ## RIRES (GOUTTES VIOLET + RIRES JAUNES)
        parleds += dmx.effet_gouttes(TEMPS_INITIAL+32.5, 14, 0.5)
        
        parleds += dmx.sequence_rires(TEMPS_INITIAL+40.4, 1, [PARLED_1.r, PARLED_1.g], [PARLED_1.r, PARLED_1.g, PARLED_1.b])
        parleds += dmx.sequence_rires(TEMPS_INITIAL+41.4, 1, [PARLED_2.r, PARLED_2.g], [PARLED_2.r, PARLED_2.g, PARLED_2.b])

        parleds += dmx.sequence_rires(TEMPS_INITIAL+48, 1, [PARLED_1.r, PARLED_1.g], [PARLED_1.r, PARLED_1.g, PARLED_1.b])
        parleds += dmx.sequence_rires(TEMPS_INITIAL+51.4, 1, [PARLED_1.r, PARLED_1.g], [PARLED_1.r, PARLED_1.g, PARLED_1.b])

        parleds += dmx.sequence_rires(TEMPS_INITIAL+55.5, 1, [PARLED_2.r, PARLED_2.g], [PARLED_2.r, PARLED_2.g, PARLED_2.b])
        parleds += dmx.sequence_rires(TEMPS_INITIAL+56, 1, [PARLED_2.r, PARLED_2.g], [PARLED_2.r, PARLED_2.g, PARLED_2.b])

        parleds += dmx.sequence_rires(TEMPS_INITIAL+46.5, 1, [PARLED_3.r , PARLED_3.g], [PARLED_3.r, PARLED_3.g, PARLED_3.b])
        parleds += dmx.sequence_rires(TEMPS_INITIAL+52.5, 1, [PARLED_3.r , PARLED_3.g], [PARLED_3.r, PARLED_3.g, PARLED_3.b])
        
        parleds += dmx.sequence_rires(TEMPS_INITIAL+50.4, 1, [PARLED_4.r , PARLED_4.g], [PARLED_4.r, PARLED_4.g, PARLED_4.b])
        parleds += dmx.sequence_rires(TEMPS_INITIAL+53.5, 1, [PARLED_4.r, PARLED_4.g], [PARLED_4.r, PARLED_4.g, PARLED_4.b])
        


        parleds += dmx.multi(TEMPS_INITIAL+60.5, dmx.fade_up_down_NEW, [PARLED_1.r, PARLED_1.b], 0.5, 20, 255, 4)
        parleds += dmx.multi(TEMPS_INITIAL+61, dmx.fade_up_down_NEW, [PARLED_2.r, PARLED_2.b], 0.5, 20, 255, 4)

        ## PREMIER CRI
        parleds.append( gevent.spawn_later(TEMPS_INITIAL+61.7, dmx.strobe, [PARLED_1.r, PARLED_1.g,\
            PARLED_1.b, PARLED_2.r, PARLED_2.g, PARLED_2.b ,PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 1, 100, 255, 15))
        parleds += dmx.multi(TEMPS_INITIAL+62.8, dmx.fade_up, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r,PARLED_2.g, PARLED_2.b,PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 0.2, 0,255, 2)
        parleds += dmx.multi(TEMPS_INITIAL+63, dmx.fade_down, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r,PARLED_2.g, PARLED_2.b,PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 2, 255, 0, 2)
        parleds.append( gevent.spawn_later(TEMPS_INITIAL+65.1, dmx.strobe, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r,PARLED_2.g, PARLED_2.b,PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 2, 100, 255, 15))

        parleds += dmx.multi(TEMPS_INITIAL+67.5,  dmx.fade_up_down_kill, [PARLED_1.r,PARLED_1.b,PARLED_2.r,PARLED_2.b,PARLED_3.r,PARLED_3.b,PARLED_4.r,PARLED_4.b], 1, 20, 255, 4, 4.7)

        parleds += dmx.effet_grad(TEMPS_INITIAL+72.5, 23, 1.5, 0.3 )

        
        parleds += dmx.inter_fade(TEMPS_INITIAL+78, 7, 0.2, [PARLED_1.r], [PARLED_1.r,PARLED_1.g, PARLED_1.b])
        parleds += dmx.inter_fade(TEMPS_INITIAL+78, 7, 0.3, [PARLED_2.r], [PARLED_2.r,PARLED_2.g, PARLED_2.b])
        parleds += dmx.inter_fade(TEMPS_INITIAL+78, 6, 0.4, [PARLED_3.r], [PARLED_3.r,PARLED_3.g,PARLED_3.b])
        parleds += dmx.inter_fade(TEMPS_INITIAL+78, 6, 0.5, [PARLED_4.r], [PARLED_4.r,PARLED_4.g,PARLED_4.b])


        parleds += dmx.multi(TEMPS_INITIAL+96, dmx.fade_down, [PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 0.5, 255, 0, 2)

        parleds += dmx.multi(TEMPS_INITIAL+95.5,  dmx.fade_up_down_kill, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r, PARLED_2.g, PARLED_2.b], 0.2, 0, 255, 8, 2.9) #fade up 0.2s phase 

        parleds += dmx.multi(TEMPS_INITIAL+97, dmx.fade_up_down_kill, [PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 0.3, 0, 255, 8, 1.5) #fade up 0.2s phase 
        parleds += dmx.multi(TEMPS_INITIAL+98.5, dmx.fade_down, [PARLED_1.r, PARLED_1.g, PARLED_1.b, PARLED_2.r, PARLED_2.g, PARLED_2.b], 2, 255, 0, 2)
        parleds += dmx.multi(TEMPS_INITIAL+98.5, dmx.fade_down, [PARLED_3.r,PARLED_3.g,PARLED_3.b,PARLED_4.r,PARLED_4.g,PARLED_4.b], 2, 255, 0, 2)


        while (len(gevent.joinall(parleds, timeout=0)) != len(parleds)) :
            foo = 42

            # j = gevent.spawn( dmx.fade_up_down_NEW, PAR_1000, 1, 0, 150, 6, 0)
            # gevent.joinall([j])

        #g3 = gevent.spawn_later(1, dmx.boucle, dmx.fade_up_down_NEW, 3, 8, 3, 100, 255)

        print ("SEQUENCE: DMX TERMINÉ")
        sleep(2)
        g_dmx.kill()

        audio_stop("sequence")
        print time()-tic
        print('EFFET: fin séquence sirènes')


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
        
        parleds = []
        parleds.extend( dmx.multi(0, dmx.battement, [2, 7,PARLED_3.r ,PARLED_4.r], duree_bat, 0, 255, 4))


        # on attend la fin du battement MAIS on INTERROMPT le battement si le lotus est touché ! 
        while (len(gevent.joinall(parleds, timeout=0)) != len(parleds)):
            sleep(.01)
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
        # dmx.valeur([2, 7, PARLED_3.r, PARLED_4.r, PAR_1000], [0,0,0,0,0])
        # dmx.blackout([2, 7, PARLED_3.r, PARLED_4.r, PAR_1000, BANDEAU_LED])
        # print("\nblackout")
        g_dmx.kill()


    def sequence_intro_caverne(self, dmx, ref_thread_events):

        audio_intro(ref_thread_events=ref_thread_events)

        g_dmx = gevent.spawn(dmx.send_serial, self.arduino_dmx, 0.03)

        g_parled_4 = gevent.spawn(dmx.constants, [PARLED_4.r, PARLED_4.g, PARLED_4.b], [10, 50, 10])

        # parleds = gevent.spawn(dmx.constant, PARLED_2.r, R-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_2.g, G-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_2.b, B-100)aaaaaaaaaaa
        # g_bandeau = []

        # parleds = gevent.spawn(dmx.constant, PARLED_3.r, R-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_3.g, G-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_3.b, B-100)

        # parleds = gevent.spawn(dmx.constant, PARLED_4.r, R-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_4.g, G-100)
        # parleds = gevent.spawn(dmx.constant, PARLED_4.b, B-100)

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
        # parleds = gevent.spawn(dmx.constant, PARLED_1.r, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_1.g, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_1.b, 0)

        # parleds = gevent.spawn(dmx.constant, PARLED_2.r, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_2.g, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_2.b, 0)
        # g_bandeau = []

        # parleds = gevent.spawn(dmx.constant, PARLED_3.r, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_3.g, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_3.b, 0)

        # parleds = gevent.spawn(dmx.constant, PARLED_4.r, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_4.g, 0)
        # parleds = gevent.spawn(dmx.constant, PARLED_4.b, 0)

        # sleep(1)
        # parleds.kill()
        # g_bandeau.kill()
        g_parled_4.kill()
        g_dmx.kill()


        