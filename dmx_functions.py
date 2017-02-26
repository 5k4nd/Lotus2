#!env/bin/python2
# -*- coding: utf-8 -*-

import gevent
#from gevent import getcurrent
from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep, time

from math import *
from data.materiel import *


interrup = trame = trame1 = [0]*30
for i in range(1,len(trame)):
    trame[i] = [0]*2




class DMX():
    """
    les fonctions DMX, en vrac.


    """

    def constant(self, channel, value):
        global trame

        while 1:
            trame[channel][0] = value
            gevent.sleep(1)

    def constants(self, channels, values):
        global trame

        while 1:
            for idx, i in enumerate(channels):
                trame[i][0] = values[idx]
            gevent.sleep(1)



    def lotus_oscillations_intro(self, bandeau_led):
        """
            attention, une couleur c'est une PROPORTION de couleurs (ici r, g et b).
            le référentiel de la boucle est donc -- en fait -- la valeur courante de la
            plus haute valeur des couleurs (réfléchissez, c'est tout bête,
            ou bidouillez pour comprendre !)


        """
        r = 30
        g = 150
        b = 50

        red_divider = int(g/r)
        blue_divider = int(g/b)


        global trame
        val_dep = 30
        pas = 2
        pause = .07

        trame[bandeau_led][0] = val_dep
        trame[bandeau_led+1][0] = val_dep
        trame[bandeau_led+2][0] = val_dep

        for i in range(val_dep, g, pas):
            trame[bandeau_led][0] = i / red_divider
            trame[bandeau_led+1][0] = i
            trame[bandeau_led+2][0] = i / blue_divider
            gevent.sleep(pause)

        gevent.sleep(1)
        
        for i in range(g, val_dep, -pas):
            trame[bandeau_led][0] = i / red_divider
            trame[bandeau_led+1][0] = i
            trame[bandeau_led+2][0] = i / blue_divider
            gevent.sleep(pause)




    """########################################################################
        les fonctions ci-dessous sont encore à nettoyer !

    """
    def zero(self):
        for i in range(1,len(trame)):
            trame[i][0] = 0


    def lotus_debut_sequence(self, bandeau_led):
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
            trame[dmx_adress][0] = i*pas_r
            trame[dmx_adress+1][0] = i*pas_g
            trame[dmx_adress+2][0] = i*pas_b
            print i*pas_r, i*pas_g, i*pas_b
            gevent.sleep(.04)
        

        gevent.sleep(1)





    def blackout(self, channels=None):
        if channels is None:
            for i in range(1, len(trame)):
                trame[i][0] = 0
        else:
            for i in channels:
                trame[i][0] = 0

    def valeur(self, channels, values):
        global trame
        j = 0
        for i in channels:
            trame[i][0] = values[j]
            j += 1




    def fade(self, channels, duree, val_dep, val_fin, pas, t=0):
        global trame, interrup
        pause = (float(duree)/abs(val_dep-val_fin))*pas
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        for i in valeurs:
            if i<=pas :
                i=0
            trame[channels][t] =  i
            gevent.sleep(pause)



    def fade_up_down(self, canal, duree, val_dep, val_fin, pas, t = 0):
        global trame
        pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        for i in valeurs:
            trame[canal][t] =  i
            gevent.sleep(pause)
        for i in reversed(valeurs):
            trame[canal][t] =  i
            gevent.sleep(pause)


    #fonction appelée régulièrement pour créer et envoyer une nouvelle trame dmx via le port série
    def send_serial(self, arduino_dmx, pause):
        global trame, interrup, trame1
        while 1:

            nb_canaux = len(trame)
            trame_envoi = ""
            for i in range(1, nb_canaux):
                if interrup[i] == 1:
                    e = trame[i][1]
                elif interrup[i] == 2 :
                    e = max(trame[i][0], trame[i][1])
                else :
                    e = trame[i][0]
                trame_envoi = trame_envoi + str(i) + "c" + str(e) + "w"
            arduino_dmx.write(trame_envoi)
            gevent.sleep(pause)

    def battement(self, channels, duree, val_dep, val_fin, pas, t = 0):
        global trame
        
        trame[PARLED_4.g][0] =  0
        trame[PARLED_4.b][0] =  0

        pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        valeurs1 = range(val_dep, val_fin, pas*2)
        for i in valeurs:
            if i <= pas :
                trame[channels][t] =  0
            else :
                trame[channels][t] =  i
            gevent.sleep(pause)

        for i in reversed(valeurs1):
            if i <= pas*2 :
                trame[channels][t] =  0
            else :
                trame[channels][t] =  i
            gevent.sleep(pause)






    def multi(self, delai, fonction, canaux, *args):
        g = [0]*len(canaux)
        j = 0
        for i in canaux:
            g[j] = gevent.spawn_later(delai, fonction, i, *args)
            j += 1
        return g

    def multi_boucle(self, delai, nombre, fonction, canaux, *args):
        g = [0]*len(canaux)
        j = 0
        dmx = DMX()
        for i in canaux:
            g[j] = gevent.spawn_later(delai, dmx.boucle, nombre, fonction, i, *args)
            j += 1
        return g







    def fade_up_down_kill(self, canal, duree, val_dep, val_fin, pas, timeout, t = 0):
        global trame
        pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        tic = time()
        while 1:
            for i in valeurs:
                trame[canal][t] =  i
                if (time() - tic > timeout) : return 0
                gevent.sleep(pause)
            for i in reversed(valeurs):
                trame[canal][t] =  i
                if (time() - tic > timeout) : return 0
                gevent.sleep(pause)

    def interruption(self, canaux, val):
        global interrup
        for i in canaux:
            interrup[i] = val

    def rire(self, delai,duree, canaux1, canaux):
        dmx = DMX()
        g = gevent.spawn_later(delai, dmx.interruption,canaux, 1)
        G = dmx.multi(delai, dmx.fade_up_down, canaux1, duree, 0, 255, 6, 1)
        g = gevent.spawn_later(delai + duree, dmx.interruption,canaux, 0)
        return G

    def inter_fade(self, delai,duree,freq, canaux1, canaux):
        dmx = DMX()
        g = gevent.spawn_later(delai, dmx.interruption,canaux, 1)
        G = dmx.multi(delai, dmx.fade_up_down_kill, canaux1, freq, 0, 255, 6, duree-0.05,1)
        g = gevent.spawn_later(delai + duree, dmx.interruption,canaux, 0)
        return G


    def strobe(self, canaux, duree, val_bas, val_haut,freq, t=0):
        global trame
        pause = 1/float(freq)
        tic = time()
        while 1:
            for i in canaux:
                trame[i][t] = val_haut
            gevent.sleep(pause)
            for i in canaux:
                trame[i][t] = val_bas
            if (time() - tic > duree) : 
                for i in canaux:
                    trame[i][t] = 0
                return 0
            gevent.sleep(pause)
        
            



    def effet_gouttes(self, delai, nombre, intervalle):
        G = []
        dmx = DMX()
        for i in range(1, nombre):
            G.extend( dmx.multi(delai, dmx.fade_up_down, [2,4], 1, 20, 255, 4))
            G.extend( dmx.multi(delai+intervalle, dmx.fade_up_down, [7,9], 1, 20, 255, 4))
            G.extend( dmx.multi(delai+intervalle*2, dmx.fade_up_down, [12,14], 1, 20, 255, 4))
            G.extend( dmx.multi(delai+intervalle*3, dmx.fade_up_down, [17,19], 1, 20, 255, 4))
            delai = delai + intervalle*4
        return G

    def effet_grad(self, delai, duree, int_dep, int_fin):
        G = []
        dmx = DMX()
        d = delai
        intervalle = int_dep
        dec = (int_dep - int_fin)/20
        while delai-d < duree:
            G.extend( dmx.multi(delai,  dmx.fade_up_down, [2,7,12,17], intervalle, 30, 100, 4))
            G.extend( dmx.multi(delai,  dmx.fade_up_down, [4,9,14,19], intervalle, 50, 255, 4))
            delai = delai + intervalle + 0.3
            intervalle = intervalle - dec
        return G

    def multi_boucle_timeout(self, delai, duree, fonction, canaux, *args):
        g = [0]*len(canaux)
        j = 0
        dmx = DMX()
        for i in canaux:
            g[j] = gevent.spawn_later(delai, dmx.boucle_timeout, duree, fonction, i, *args)
            j += 1
        return g

    def boucle_timeout(self, duree, fonction, *args):
        tic = time()
        while (time() - tic < duree):
            fonction(*args)


    def boucle(self, nombre, fonction, *args):
        for i in range(0, nombre):
            fonction(*args)



    def attente(self, duree, capteur):
        pause = 0.1
        fin = 0
        tic = time()
        while (time() - tic < duree) and (capteur == false):
            gevent.sleep(0.1)

