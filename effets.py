#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gevent

from gevent.pool import Group
from time import sleep, time

from audio_functions import *
from data.materiel import *
from dmx_functions import *



class Effets():
    """
        dans cette classe se trouvent tous les effets.
        un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son d'audio_functions

    """

    def __init__(self, arduino_dmx, arduino_ultrasonics, arduino_lotus):
        self.arduino_dmx = arduino_dmx
        self.arduino_ultrasonics = arduino_ultrasonics
        self.arduino_lotus = arduino_lotus




    def sequence(self, ref_thread_events):
        """
            la séquence principale des sirènes, chronologiquement par effet lumière
            et accessoirement effets sonores

            voir le premier appel de la méthode add_effect pour un aperçu de ses différents paramètres.

            vous pouvez travailler à partir d'un temps spécifique en modifiant la constante STARTING_TIME à autre chose que 0.

        """


        """
        ####################################################################
                        QUELQUES FONCTIONS POUR LA SÉQUENCE
        ####################################################################
        """


        def add_effect(equipment, starting_time, dmx_channels, effect, effect_args, overrided_channels=None, repeat=1):
            starting_time += STARTING_TIME

            # s'il y a des canaux à haut niveau de priorité on démarre un thread prioritaire pour le flux DMX
            if overrided_channels:
                print "ADD_EFFECT: OVERRIDE EN COURS"
                override_duration = effect_args[0]  # un peu pourri comme pratique
                current_dmx_frame = priority_dmx_frame
                overrider = gevent.spawn_later(starting_time, dmx_high_priority_overrider, current_dmx_frame, overrided_channels, True)
            # sinon c'est le flux DMX normal
            else:    
                current_dmx_frame = dmx_frame

            # génère un thread par canal, avec des répétitions de fonctions si demandé
            for times in range(repeat):
                for channel in dmx_channels:        
                    equipment.append(
                        gevent.spawn_later(starting_time, effect, current_dmx_frame, channel, *effect_args)
                    )
        
            # s'il y avait des canaux à haut niveau de priorité on arrête le thread prioritaire pour le flux DMX
            if overrided_channels:
                overrider = gevent.spawn_later(starting_time + override_duration, dmx_high_priority_overrider, current_dmx_frame, overrided_channels, False)
                print "ADD_EFFECT: FIN D'UN OVERRIDE"

        def add_simple_effect(equipment, starting_time, effect, effect_args):
            """
                more transparency than add_effect, more freedom for users' calls.
            """
            starting_time += STARTING_TIME

            equipment.append(
                gevent.spawn_later(starting_time, effect, dmx_frame, *effect_args)
            )

        def laughs_effect(start_time, times_number, interval):
            for i in range(1, times_number):
                add_effect(parleds, start_time,            [PARLED_1.r, PARLED_1.b], fade_up_down, [1, 20, 255, 4])
                add_effect(parleds, start_time+interval,   [PARLED_2.r, PARLED_2.b], fade_up_down, [1, 20, 255, 4])
                add_effect(parleds, start_time+interval*2, [PARLED_3.r, PARLED_3.b], fade_up_down, [1, 20, 255, 4])
                add_effect(parleds, start_time+interval*3, [PARLED_4.r, PARLED_4.b], fade_up_down, [1, 20, 255, 4])
                start_time = start_time + interval*4

        def petite_explosion(starting_time):
            """
                à reprendre !
            """
            add_effect(parleds, 20.3,   [PARLED_2.r], fade_up_down, [0.8, 50, 255, 6])
            add_effect(parleds, 20.5,   [PARLED_2.b], fade_up, [1, 0, 255, 2])
            add_effect(parleds, 21.5,   [PARLED_2.r, PARLED_2.b], fade_down, [0.5, 255, 0, 4])



        def effet_palpitation_graduelle(dmx_frame, starting_time, duration, int_dep, int_fin):
            """
                palpite de plus en plus vite.
            """
            d = starting_time
            interval = int_dep
            dec = (int_dep - int_fin)/20
            while starting_time-d < duration:
                add_effect(parleds, starting_time,  PARLED_ALL.r, fade_up_down, [interval, 30, 100, 4])
                add_effect(parleds, starting_time,  PARLED_ALL.b, fade_up_down, [interval, 50, 255, 4])
                starting_time = starting_time + interval + 0.3
                interval = interval - dec

        """
        ####################################################################
                            INITIALISATION DE LA SÉQUENCE
        ####################################################################
        """
        # audio_sequence(ref_thread_events)

        STARTING_TIME = 0  # used for debugging
        
        dmx_frame, priority_dmx_frame, dmx_streamer = init_dmx(arduino_dmx=self.arduino_dmx, max_dmx_channels=30)
        blackout(dmx_frame)

        parleds = []




        """
        ####################################################################
                    LA SÉQUENCE i.e. tous les effets à la suite
        ####################################################################
        """
        ## INTRO
        add_effect(
            equipment=parleds,
            starting_time=0,
            dmx_channels=[PARLED_1.b, PARLED_2.b],
            effect=fade_up,
            effect_args=[0.2, 0, 255, 6],
            overrided_channels=None,    # optional
            repeat=1                    # optional
        )
        add_effect(parleds, 0.5,    [PARLED_1.r, PARLED_1.g, PARLED_2.r, PARLED_2.g], fade_up, [1, 0, 255, 4])
        add_effect(parleds, 1.2,    PARLED_1.rgb+PARLED_2.rgb, fade_up_down, [0.2, 0, 255, 8, 3.8])

        add_effect(parleds, 0,      [PARLED_3.r, PARLED_4.r], fade_up_down, [0.8, 0, 255, 8])
        add_effect(parleds, 0,      [PARLED_3.b, PARLED_4.b], fade_up_down, [0.8, 0, 255, 8])        
        add_effect(parleds, 3,      PARLED_3.rgb+PARLED_4.rgb, fade_up_down, [0.3, 0, 255, 8, 2])
        
        add_effect(parleds, 5,      PARLED_1.rgb+PARLED_2.rgb, fade_down, [2, 255, 0, 2])
        add_effect(parleds, 5,      PARLED_3.rgb+PARLED_4.rgb, fade_down, [2.2, 255, 0, 2])

        

        ## premières paroles (VIOLET)
        add_effect(parleds, 9.2,    [PARLED_1.r, PARLED_1.b], fade_up, [0.3, 0, 50, 4])
        add_effect(parleds, 9.5,    [PARLED_1.r, PARLED_1.b], fade_up_down, [2.9, 50, 255, 4], repeat=3)
        add_effect(parleds, 19,     [PARLED_1.r, PARLED_1.b], fade_down, [0.2, 50, 0, 4])
        add_effect(parleds, 13.2,   [PARLED_2.r, PARLED_2.b], fade_up, [0.3, 0, 50, 4])
        add_effect(parleds, 13.5,   [PARLED_2.r, PARLED_2.b], fade_up_down, [2, 50, 255, 4], repeat=2)
        add_effect(parleds, 18,     [PARLED_2.r, PARLED_2.b], fade_down, [1, 50, 0, 2])


        # HARPE - suite des paroles (BLEU)
        add_effect(parleds, 19,     [PARLED_1.b], fade_up,   [1, 0, 255, 2])
        add_effect(parleds, 20,     [PARLED_1.b], fade_down, [0.5, 255, 0, 5])
        add_effect(parleds, 25,     [PARLED_1.b], fade_up,   [1, 0, 255, 2])
        add_effect(parleds, 26,     [PARLED_1.b], fade_down, [0.5, 255, 0, 4])
        
        add_effect(parleds, 20.5,   [PARLED_2.b], fade_up,   [1, 0, 255, 2])
        add_effect(parleds, 21.5,   [PARLED_2.b], fade_down, [0.5, 255, 0, 4])
        add_effect(parleds, 26.5,   [PARLED_2.b], fade_up,   [1, 0, 255, 4])
        add_effect(parleds, 27.5,   [PARLED_2.b], fade_down, [0.5, 255, 0, 2])

        add_effect(parleds, 22,     [PARLED_3.b], fade_up,   [1, 0, 255, 2])
        add_effect(parleds, 23,     [PARLED_3.b], fade_down, [0.5, 255, 0, 4])

        add_effect(parleds, 23.5,   [PARLED_4.b], fade_up,   [1, 0, 255, 2])
        add_effect(parleds, 24.5,   [PARLED_4.b], fade_down, [0.5, 255, 0, 4])

        ## fade up down rose
        add_effect(parleds, 28,     PARLED_ALL.r+PARLED_ALL.b, fade_up,   [2, 0,255, 4])
        add_effect(parleds, 30,     PARLED_ALL.r+PARLED_ALL.b, fade_down, [0.4, 255, 0, 4])

        ## éclat rouge
        add_effect(parleds, 30.5,   PARLED_ALL.r, fade_up,   [1, 0,255, 2])
        add_effect(parleds, 31.5,   PARLED_ALL.r, fade_down, [1, 255,0, 2])
        add_simple_effect(parleds, 32.5, constants, [[PARLED_1.r, PARLED_1.b], [0, 0]])


        ## RIRES (GOUTTES VIOLET + RIRES JAUNES)
        laughs_effect(32.5, 14, 0.5)

        # simule des rires, qui prennent le dessus sur tout le reste (via le paramètre override_param)
        add_effect(parleds, 40.4,   [PARLED_1.r, PARLED_1.g], fade_up_down, [1, 0, 255, 6], overrided_channels=PARLED_1.rgb)
        add_effect(parleds, 48,     [PARLED_1.r, PARLED_1.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_1.rgb)
        add_effect(parleds, 51.4,   [PARLED_1.r, PARLED_1.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_1.rgb)

        add_effect(parleds, 41.4,   [PARLED_2.r, PARLED_2.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_2.rgb)
        add_effect(parleds, 55.5,   [PARLED_2.r, PARLED_2.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_2.rgb)
        add_effect(parleds, 56,     [PARLED_2.r, PARLED_2.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_2.rgb)

        add_effect(parleds, 46.5,   [PARLED_3.r, PARLED_3.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_3.rgb)
        add_effect(parleds, 52.5,   [PARLED_3.r, PARLED_3.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_3.rgb)
        
        add_effect(parleds, 50.4,   [PARLED_4.r, PARLED_4.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_4.rgb)
        add_effect(parleds, 53.5,   [PARLED_4.r, PARLED_4.g], fade_up_down, [1, 0, 266, 6], overrided_channels=PARLED_4.rgb)
        
        add_effect(parleds, 60.5,   [PARLED_1.r, PARLED_1.b], fade_up_down, [0.5, 20, 255, 4])
        add_effect(parleds, 61,     [PARLED_2.r, PARLED_2.b], fade_up_down, [0.5, 20, 255, 4])

        ## PREMIER CRI
        add_simple_effect(parleds, 61.7, strobe, [PARLED_ALL.rgb, 1, 100, 255, 15])
        add_effect(parleds, 62.8,   PARLED_ALL.rgb, fade_up, [0.2, 0,255, 2])
        add_effect(parleds, 63,     PARLED_ALL.rgb, fade_down, [2, 255, 0, 2])
        add_simple_effect(parleds, 65.1, strobe, [PARLED_ALL.rgb, 2, 100, 255, 15])

        add_effect(parleds, 67.5,  PARLED_ALL.r + PARLED_ALL.b, fade_up_down, [1, 20, 255, 4])


        ## DÉBUT CRESCENDO FINAL
        effet_palpitation_graduelle(dmx_frame, 72.5, 23, 1.5, 0.3)
        
        ## clignotements rouges rapides
        add_effect(parleds, 78,     [PARLED_1.r], fade_up_down, [0.2, 0, 255, 6, 6.95], overrided_channels=PARLED_1.rgb)
        add_effect(parleds, 78,     [PARLED_2.r], fade_up_down, [0.3, 0, 255, 6, 6.95], overrided_channels=PARLED_2.rgb)
        add_effect(parleds, 78,     [PARLED_3.r], fade_up_down, [0.4, 0, 255, 6, 5.95], overrided_channels=PARLED_3.rgb)
        add_effect(parleds, 78,     [PARLED_4.r], fade_up_down, [0.5, 0, 255, 6, 5.95], overrided_channels=PARLED_4.rgb)


        # ## vortex final (majoritairement blanc)
        add_effect(parleds, 96,     PARLED_3.rgb + PARLED_4.rgb, fade_down, [0.5, 255, 0, 2])

        add_effect(parleds, 95.5,   PARLED_1.rgb + PARLED_2.rgb, fade_up_down, [0.2, 0, 255, 8, 2.9])
        add_effect(parleds, 97,     PARLED_3.rgb + PARLED_4.rgb, fade_up_down, [0.3, 0, 255, 1.5])

        add_effect(parleds, 98.5,   PARLED_1.rgb + PARLED_2.rgb, fade_down, [2, 255, 0, 2])
        add_effect(parleds, 98.5,   PARLED_3.rgb + PARLED_4.rgb, fade_down, [2, 255, 0, 2])

        # on laisse le temps au dmx de s'écouler proprement
        parleds .append(gevent.spawn_later(99, gevent.sleep(2)))
        
        while (len(gevent.joinall(parleds, timeout=0)) != len(parleds)) :
            foo = 42
            # pc_1000 = gevent.spawn( fade_up_down, PC_1000, 1, 0, 150, 6, 0)
            # gevent.joinall([pc_1000])

        print ("SEQUENCE: DMX TERMINÉ")

        sleep(2)
        dmx_streamer.kill()

        audio_stop("sequence")

        # print time()-tic
        print('SEQUENCE: fin séquence sirènes')


    def battement_de_coeur(self, ref_thread_events):
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

        dmx_frame, priority_dmx_frame, dmx_streamer = init_dmx(arduino_dmx=self.arduino_dmx, max_dmx_channels=30)
        
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
        dmx_streamer.kill()


    def sequence_intro_caverne(self, ref_thread_events):

        audio_intro(ref_thread_events=ref_thread_events)

        dmx_frame, priority_dmx_frame, dmx_streamer = init_dmx(arduino_dmx=self.arduino_dmx, max_dmx_channels=30)
        # dmx_streamer = gevent.spawn(send_serial, self.arduino_dmx, 0.03)

        g_parled_4 = gevent.spawn(constants, dmx_frame, PARLED_4.rgb, [10, 50, 10])

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
            g_bandeau = gevent.spawn(intro_lotus_oscillations, dmx_frame, BANDEAU_LED.r)
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
        dmx_streamer.kill()


        