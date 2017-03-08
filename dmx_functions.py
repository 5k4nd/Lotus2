#!env/bin/python2
# -*- coding: utf-8 -*-

"""
    ce fichier regroupe toutes les fonctions DMX, notamment les effets de lumière.

    Le développeur attentif remarquera que gevent, c'est pas fait pour
    l'évenementiel : tu demandes une pause de 0.034 secondes, il t'en fait
    une de 0.45 secondes. bah du coup faut bidouiller. des bonbons à celui qui
    trouve le moyen de contourner ce souci sans tout recoder en C++ ;-) 

ToDo:
- faire une fonction dmx_run(priority={low, normal, high}})
    et si high voir rires() et inter_fade

"""

import gevent

from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep, time

from math import *
from data.equipment import *
from data.colors import *







"""########################################################################
    les méthodes ci-dessous sont des méthodes techniques.

"""

def init_dmx(arduino_dmx, max_dmx_channels):
    MAX_DMX_CHANNELS = max_dmx_channels

    dmx_frame          = [0]*MAX_DMX_CHANNELS
    priority_dmx_frame = [-1]*MAX_DMX_CHANNELS  # convention : la valeur par défaut du dmx_frame à haut niveau de priorité est -1
    # for i in range(0,len(dmx_frame)):
    #     dmx_frame[i] = [0]*2
        # priority_dmx_frame[i] = [-1]*2

    dmx_streamer = gevent.spawn(send_serial, arduino_dmx, 0.02, dmx_frame, priority_dmx_frame)
    # dmx_streamer = 'foobar'
    return dmx_frame, priority_dmx_frame, dmx_streamer

def send_serial(arduino_dmx, pause, dmx_frame, priority_dmx_frame):

    """
        FONCTION PRINCIPALE 
            appelée régulièrement pour créer et envoyer une nouvelle trame dmx via le port série.
            lorsqu'une fonction dmx a besoin d'écraser une fonction en court, il faut utiliser le
            champ "interrup" à 1 (voire 2, cf le code ci-dessous).
    """
    # global dmx_frame, interrup
    while 1:
        sleep(.0001)
        nb_canaux = len(dmx_frame)
        trame_envoi = ""
        for i in range(0, nb_canaux):
            if priority_dmx_frame[i] != -1:
                e = priority_dmx_frame[i]
            else:
                e = dmx_frame[i]
            trame_envoi = trame_envoi + str(i) + "c" + str(e) + "w"
        arduino_dmx.write(trame_envoi)
        gevent.sleep(pause)


def dmx_high_priority_overrider(priority_dmx_frame, overrided_channels, run):
    if run:
        for channel in overrided_channels: priority_dmx_frame[channel] = 0
    else:
        for channel in overrided_channels: priority_dmx_frame[channel] = -1







"""
############################################################################
                            DMX EFFECTS ON CHANNELS
############################################################################
"""


def fade_up(dmx_frame, channel, duration, val_dep, val_fin, pas, t=0):


    nb_frames = float(val_fin - val_dep) / pas
    # print nb_frames
    frame_per_second = ceil( float(nb_frames) / duration )
    # print frame_per_second
    pause = 1.0 / frame_per_second
    # print pause

    tic = time()
    for idx, i in enumerate(range(val_dep, val_fin, pas)):
        if idx > 0:
            gevent.sleep(pause)
        if i + pas > val_fin:  # car range ne permet pas toujours d'aller au bout
            dmx_frame[channel] = val_fin
        else:
            dmx_frame[channel] = i

    if float(time()-tic) > float(duration):
        print "EFFET WARNING: fade up down trop long %s au lieu de %s" % (round(time()-tic, 2), duration)

def fade_down(dmx_frame, channels, duration, val_dep, val_fin, pas, t=0):

    nb_frames = float(val_dep - val_fin) / pas
    # print nb_frames
    frame_per_second = ceil( float(nb_frames) / duration )
    # print frame_per_second
    pause = 1.0 / frame_per_second
    # print pause

    tic = time()
    for idx, i in enumerate(range(val_dep, val_fin-1, -pas)):  # attention au -1 pour inclure les bornes de l'intervalle
        if idx > 0:
            gevent.sleep(pause)
        if i - pas < val_fin:  # car range ne permet pas toujours d'aller au bout
            dmx_frame[channels] = val_fin
        else:
            dmx_frame[channels] = i
        # print dmx_frame[channels]

    if float(time()-tic) > float(duration):
        print "EFFET WARNING: fade down trop long %s au lieu de %s (channels %s)" % (round(time()-tic, 2), duration, channels)


def fade_up_down(dmx_frame, channel, duration, val_dep, val_fin, pas, timeout=None):
    """
        cette méthode peut prendre un paramètre optionnel timeout. dans ce cas elle tourne en boucle jusqu'au timeout.
    
    """
    nb_frames = float(val_fin - val_dep) / pas

    frame_per_second = ceil( float(nb_frames) / duration )
    pause = 1.0 / frame_per_second

    pause /= 2  # car on a deux boucles

    values = range(val_dep, val_fin+1, pas)
    tic = time()

    must_go_on = True
    while must_go_on:
        for idx, value in enumerate(values):
            # if (time() - tic > timeout) : return 0
            # nécessaire pour ne pas faire le dernier sleep de la boucle
            if idx > 1:
                gevent.sleep(pause)
            dmx_frame[channel] = value

        for idx, value in enumerate(reversed(values)):
            # if (time() - tic > timeout) : return 0
            if idx > 1:
                gevent.sleep(pause)
            dmx_frame[channel] =  value
        
        # if we have to follow a timeout parameter
        if timeout:
            if (time() - tic > timeout):
                # we can exit
                must_go_on=False
        # else we don't have any timeout parameter, we can exit
        else:
            must_go_on=False


    if float(time()-tic) > float(duration):
        print "EFFET WARNING: fade up down trop long %s au lieu de %s" % (round(time()-tic, 2), duration)


def strobe(dmx_frame, channels, duration, lower_value, upper_value, freq):
    pause = 1/float(freq)

    tic = time()
    while 1:
        for channel in channels:
            dmx_frame[channel] = upper_value
        # gevent.sleep(pause)
        for channel in channels:
            dmx_frame[channel] = lower_value
        if (time() - tic > duration) : 
            for channel in channels:
                dmx_frame[channel] = 0
            return 0
        # gevent.sleep(pause)
        






def constants(dmx_frame, channels, values):
    if isinstance(values, int):
        # then our user, just pass a single value for all channels
        values = values*len(channels)    
    for idx, channel in enumerate(channels):
        dmx_frame[channel] = values[idx]
    gevent.sleep(1)


def blackout(dmx_frame, channels=None):
    """
        reset les canaux passés en paramètre à 0 ; par défaut, RESET LES 512 CANAUX.
    """

    if channels is None:
        for dmx_channel in range(1, equipment_adresse_max+1):
            dmx_frame[dmx_channel] = 0
    else:
        for dmx_channel in channels:
            dmx_frame[dmx_channel] = 0


# def valeur(self, channels, values):
#     global trame
#     j = 0
#     for i in channels:
#         trame[i] = values[j]
#         j += 1











"""
############################################################################
                        DMX COMPLEX LOOPS
############################################################################
"""

def intro_lotus_oscillations(dmx_frame, bandeau_led):
    """
    Note 1 :
        attention, une couleur c'est une PROPORTION de couleurs (ici r, g et b).
        le référentiel de la boucle est donc -- en fait -- la valeur courante de la
        plus haute valeur des couleurs (réfléchissez, c'est tout bête,
        ou bidouillez pour comprendre !)

    Note 2 :         
        attention, les boucles sont en deux parties car la partie des valeurs de
        couleurs basses ont un pas plus faible (c'est plus fluide visuellement !).

    """


    r, g, b = rose_lotus
    
    green_divider = int(r/g)
    blue_divider = int(r/b)


    val_dep = 26
    pas = 2
    pause=.04

    val_intermediaire = 66
    pas_rapide = 1
    pause_rapide = pause / 4.0


    # # constantes pour tests
    # dmx_frame[bandeau_led] = 70
    # dmx_frame[bandeau_led+1] = 70
    # dmx_frame[bandeau_led+2] = 70
    # sleep(.001)


    # boucle d'oscillation ascendante 1
    for i in range(val_dep, val_intermediaire, pas_rapide):
        dmx_frame[bandeau_led] = i
        dmx_frame[bandeau_led+1] = i / green_divider
        dmx_frame[bandeau_led+2] = i / blue_divider
        gevent.sleep(pause_rapide)

    # boucle d'oscillation ascendante 2
    for i in range(val_intermediaire, r, pas):
        dmx_frame[bandeau_led] = i
        dmx_frame[bandeau_led+1] = i / green_divider
        dmx_frame[bandeau_led+2] = i / blue_divider
        gevent.sleep(pause)


    gevent.sleep(2)

    # boucle d'oscillation descendante 1
    for i in range(r, val_intermediaire, -pas):
        dmx_frame[bandeau_led] = i
        dmx_frame[bandeau_led+1] = i / green_divider
        dmx_frame[bandeau_led+2] = i / blue_divider
        gevent.sleep(pause)
    
    # boucle d'oscillation descendante 2
    for i in range(val_intermediaire, val_dep, -pas_rapide):
        dmx_frame[bandeau_led] = i
        dmx_frame[bandeau_led+1] = i / green_divider
        dmx_frame[bandeau_led+2] = i / blue_divider
        gevent.sleep(pause_rapide)


def intro_battement(dmx_frame, bandeau_led, ref_must_start_sequence, level):
    """
        le mieux dans cette fonction, c'est de faire varier le "rythme cardiaque"
        avec sleep_oscillation. comme ça le battement en tant que tel est calé sur
        le son, c'est plus simple. ;-)
    """
    if level == 1:
        sleep_oscillation = .1
    if level == 2:
        sleep_oscillation = .02
   
    duree = 0.35
    min_value = 60
    max_value = 250
    inter_value = 30
    pas = 8
    pause = .05


    # palpitation
    for i in range(min_value, max_value, pas):
        print i
        dmx_frame[bandeau_led] = i
        gevent.sleep(pause)

    for i in range(max_value, min_value, -pas):
        print i
        dmx_frame[bandeau_led] = i
        gevent.sleep(pause)


    # # oscillation lente
    # for i in range(min_value, inter_value, -2):
    #     print i
    #     dmx_frame[bandeau_led] = i
    #     gevent.sleep(sleep_oscillation)

    # for i in range(inter_value, min_value, 2):
    #     print i
    #     dmx_frame[bandeau_led] = i
    #     gevent.sleep(sleep_oscillation)



















class DMX():
    """
        à déplacer hors de la classe.
    """

    def sequence_lotus_vortex(self, dmx_adress):
        """
            lotus multicolore au démarrage de la séquence (c'est le poison des lotophages)

        """

        global trame
        val_dep = 10

        pas_r = 105 / 3
        pas_g = 162 / 3
        pas_b = 120 / 3

        val_fin = (r - val_dep) / pas_r
        temps_pause = (float(duration) / abs(val_dep - val_fin)) * pas_r

        for i in range(0, r, 3):
            # print i
            trame[dmx_adress] = i*pas_r
            trame[dmx_adress+1] = i*pas_g
            trame[dmx_adress+2] = i*pas_b
            print i*pas_r, i*pas_g, i*pas_b
            gevent.sleep(.04)
        

        gevent.sleep(1)








    # def multi_boucle_timeout(self, delai, duree, fonction, canaux, *args):
    #     g = [0]*len(canaux)

    #     dmx = DMX()
    #     for idx, i in enumerate(canaux):
    #         g[idx] = gevent.spawn_later(delai, dmx.boucle_timeout, duree, fonction, i, *args)

    #     return g

    # def boucle_timeout(self, duree, fonction, *args):
    #     tic = time()
    #     while (time() - tic < duree):
    #         fonction(*args)


    # def attente(self, duree, capteur):
    #     pause = 0.1
    #     fin = 0
    #     tic = time()
    #     while (time() - tic < duree) and (capteur == false):
    #         gevent.sleep(0.1)

    # def fade_up_down(self, canal, duree, val_dep, val_fin, pas, t = 0):
    #     """ méthode à supprimer"""

    #     global trame
    #     pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))

    #     if val_dep > val_fin :
    #         valeurs = range(val_dep,val_fin, -pas)
    #     else : valeurs = range(val_dep, val_fin, pas)
    #     for i in valeurs:
    #         trame[canal] =  i
    #         gevent.sleep(pause)
    #     for i in reversed(valeurs):
    #         trame[canal] =  i
    #         gevent.sleep(pause)
  
  
    # def fade_up_down_kill(self, canal, duree, val_dep, val_fin, pas, timeout, t = 0):
    #     global trame
    #     pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
    #     if val_dep > val_fin :
    #         valeurs = range(val_dep,val_fin, -pas)
    #     else : valeurs = range(val_dep, val_fin, pas)
    #     tic = time()
    #     while 1:
    #         for i in valeurs:
    #             trame[canal] =  i
    #             if (time() - tic > timeout) : return 0
    #             gevent.sleep(pause)
    #         for i in reversed(valeurs):
    #             trame[canal] =  i
    #             if (time() - tic > timeout) : return 0
    #             gevent.sleep(pause)






    # def fade(self, channels, duree, val_dep, val_fin, pas, t=0):
    #     global trame

    #     pause = (float(duree)/abs(val_dep-val_fin))*pas

    #     if val_dep > val_fin :
    #         valeurs = range(val_dep,val_fin, -pas)
    #     else:
    #         valeurs = range(val_dep, val_fin, pas)

    #     for i in valeurs:
    #         if i<=pas :
    #             i=0
    #         trame[channels] =  i
    #         gevent.sleep(pause)




# def constant(self, channel, value):
#     global trame

#     trame[channel][0] = value
#     gevent.sleep(1)




# def effet_gouttes(dmx_frame, number, interval):
# parleds = []

# for i in range(1, number):
#     parleds.extend( dmx.multi(delay, dmx.fade_up_down,            [PARLED_1.r, PARLED_1.b], 1, 20, 255, 4))
#     parleds.extend( dmx.multi(delay+interval, dmx.fade_up_down,   [PARLED_2.r, PARLED_2.b], 1, 20, 255, 4))
#     parleds.extend( dmx.multi(delay+interval*2, dmx.fade_up_down, [PARLED_3.r, PARLED_3.b], 1, 20, 255, 4))
#     parleds.extend( dmx.multi(delay+interval*3, dmx.fade_up_down, [PARLED_4.r, PARLED_4.b], 1, 20, 255, 4))
#     delay = delay + interval*4
# return parleds

# def effet_gouttes(dmx_frame, starting_time, number, interval):

#     equipment_extension = []
#     equipment_extension.append(gevent.spawn_later(starting_time, fade_up_down, dmx_frame, [PARLED_1.r], 1, 20, 255, 4))
#     # for i in range(1, number):
#     #     parleds_extension.extend( dmx.multi(starting_time, fade_up_down,            [PARLED_1.r, PARLED_1.b], 1, 20, 255, 4))
#     #     parleds_extension.extend( dmx.multi(starting_time+interval, fade_up_down,   [PARLED_2.r, PARLED_2.b], 1, 20, 255, 4))
#     #     parleds_extension.extend( dmx.multi(starting_time+interval*2, fade_up_down, [PARLED_3.r, PARLED_3.b], 1, 20, 255, 4))
#     #     parleds_extension.extend( dmx.multi(starting_time+interval*3, fade_up_down, [PARLED_4.r, PARLED_4.b], 1, 20, 255, 4))
#     #     starting_time = starting_time + interval*4



#         # print "number", i
#         # for channel in [PARLED_1.r, PARLED_1.b]:
#         #     equipment_extension.append(gevent.spawn_later(starting_time, fade_up_down, dmx_frame, channel, 1, 20, 255, 4))
#         # for channel in [PARLED_2.r, PARLED_2.b]:
#         #     equipment_extension.append(gevent.spawn_later(starting_time+interval, fade_up_down, dmx_frame, channel, 1, 20, 255, 4))
#         # for channel in [PARLED_3.r, PARLED_3.b]:
#         #     equipment_extension.append(gevent.spawn_later(starting_time+interval*2, fade_up_down, dmx_frame, channel, 1, 20, 255, 4))
#         # for channel in [PARLED_4.r, PARLED_4.b]:
#         #     equipment_extension.append(gevent.spawn_later(starting_time+interval*3, fade_up_down, dmx_frame, channel, 1, 20, 255, 4))
#         # starting_time = starting_time + interval*4

#         # parleds_extension.extend( dmx.multi(delay, dmx.fade_up_down,            [PARLED_1.r, PARLED_1.b], 1, 20, 255, 4))
#         # parleds_extension.extend( dmx.multi(delay+interval, dmx.fade_up_down,   [PARLED_2.r, PARLED_2.b], 1, 20, 255, 4))
#         # parleds_extension.extend( dmx.multi(delay+interval*2, dmx.fade_up_down, [PARLED_3.r, PARLED_3.b], 1, 20, 255, 4))
#         # parleds_extension.extend( dmx.multi(delay+interval*3, dmx.fade_up_down, [PARLED_4.r, PARLED_4.b], 1, 20, 255, 4))
#         # delay = delay + interval*4
#     return equipment_extension






    # def boucle(self, iterations, function, *args):
    #     """
    #         lance la fonction demandée un nombre "iterations" de fois.
    #     """
    #     for i in range(0, iterations):
    #         function(*args)

    # def multi_boucle(self, delay, iterations, function, channels, *args):
    #     """
    #         on duplique la fonciton demandée et on la lance un nombre "iterations" de fois.

    #     """
    #     g = [0]*len(channels)
        
    #     dmx = DMX()
    #     for idx, channel in enumerate(channels):
    #         g[idx] = gevent.spawn_later(delay, dmx.boucle, iterations, function, channel, *args)

    #     return g



# def effet_grad(dmx_frame, delai, duree, int_dep, int_fin):
#     G = []
#     dmx = DMX()
#     d = delai
#     intervalle = int_dep
#     dec = (int_dep - int_fin)/20
#     while delai-d < duree:
#         G.extend( dmx.multi(delai,  dmx.fade_up_down, [2,7,12,17], intervalle, 30, 100, 4))
#         G.extend( dmx.multi(delai,  dmx.fade_up_down, [4,9,14,19], intervalle, 50, 255, 4))
#         delai = delai + intervalle + 0.3
#         intervalle = intervalle - dec
#     return G


# def sequence_rires(self, delay, duration, channels, overrided_channels):
#     dmx = DMX()
#     g = gevent.spawn_later(delay, dmx.override, overrided_channels, 1)
#     parleds = dmx.multi(delay, dmx.fade_up_down, channels, duration, 0, 255, 6, 1)
#     g = gevent.spawn_later(delay + duration, dmx.override, overrided_channels, 0)
#     return parleds
# def inter_fade(delay, duration, freq, channels, overrided_channels):
#     dmx = DMX()
#     g = gevent.spawn_later(delay, dmx.override, overrided_channels, 1)
#     parleds = dmx.multi(delay, dmx.fade_up_down_kill, channels, freq, 0, 255, 6, duration-0.05,1)
#     g = gevent.spawn_later(delay + duration, dmx.override, overrided_channels, 0)
#     return parleds

# def multi( delay, function, channels, *args):
#     """
#         duplique la fonction demandée pour chaque canal passé en paramètre.

#     """

#     g = [0]*len(channels)

#     for idx, channel in enumerate(channels):
#         g[idx] = gevent.spawn_later(delay, function, channel, *args)

#     return g



# def fade_up_down_kill(dmx_frame, canal, duree, val_dep, val_fin, pas, timeout):
#     pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
#     if val_dep > val_fin :
#         valeurs = range(val_dep,val_fin, -pas)
#     else : valeurs = range(val_dep, val_fin, pas)
#     tic = time()
#     while 1:
#         for i in valeurs:
#             dmx_frame[canal][0] =  i
#             if (time() - tic > timeout) : return 0
#             gevent.sleep(pause)
#         for i in reversed(valeurs):
#             dmx_frame[canal][0] =  i
#             if (time() - tic > timeout) : return 0
#             gevent.sleep(pause)



# def send_serial(arduino_dmx, pause, dmx_frame, priority_dmx_frame):
#     # global dmx_frame, interrup
#     while 1:

#         nb_canaux = len(dmx_frame)
#         trame_envoi = ""
#         for i in range(0, nb_canaux):
#             # if interrup[i] == 1:
#             #     e = dmx_frame[i][1]
#             # elif interrup[i] == 2 :
#             #     e = max(dmx_frame[i], dmx_frame[i][1])
#             # else :
#             e = dmx_frame[i]
#             trame_envoi = trame_envoi + str(i) + "c" + str(e) + "w"
#         arduino_dmx.write(trame_envoi)
#         gevent.sleep(pause)


# def fade_up_down(dmx_frame, channel, duration, val_dep, val_fin, pas, t = 0):

#     nb_frames = float(val_fin - val_dep) / pas
#     # print nb_frames
#     frame_per_second = ceil( float(nb_frames) / duration )
#     pause = 1.0 / frame_per_second

#     pause /= 2  # car on a deux boucles

#     values = range(val_dep, val_fin+1, pas)
#     tic = time()
#     for idx, value in enumerate(values):
#         if idx > 1:  # nécessaire pour ne pas faire le dernier sleep
#             gevent.sleep(pause)
#             dmx_frame[channel] = value
#     for (idx, i) in enumerate(reversed(values)):
#         if idx > 1:
#             gevent.sleep(pause)
#         dmx_frame[channel] =  i

#     if float(time()-tic) > float(duration):
#         print "EFFET WARNING: fade up down trop long %s au lieu de %s" % (round(time()-tic, 2), duration)


