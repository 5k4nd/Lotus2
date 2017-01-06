#!env/bin/python2
# -*- coding: utf-8 -*-
import gevent
#from gevent import getcurrent
from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep
import time
from math import *
interrup = [0]*25
trame = [0]*25
trame1 = [0]*25
for i in range(1,len(trame)):
    trame[i] = [0]*2

class DMX():

    #battement linéaire (limité en fréquence à 0.1s environ)
    def zero(self):
        for i in range(1,len(trame)):
            trame[i][0] = 0

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

    def fade_up_down_kill(self, canal, duree, val_dep, val_fin, pas, timeout, t = 0):
        global trame
        pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        tic = time.time()
        while 1:
            for i in valeurs:
                trame[canal][t] =  i
                if (time.time() - tic > timeout) : return 0
                gevent.sleep(pause)
            for i in reversed(valeurs):
                trame[canal][t] =  i
                if (time.time() - tic > timeout) : return 0
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

    def fade(self, canal, duree, val_dep, val_fin, pas, t=0):
        global trame, interrup
        pause = (float(duree)/abs(val_dep-val_fin))*pas
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        for i in valeurs:
            if i<=pas :
                i=0
            trame[canal][t] =  i
            gevent.sleep(pause)

    def strobe(self, canaux, duree, val_bas, val_haut,freq, t=0):
        global trame
        pause = 1/float(freq)
        tic = time.time()
        while 1:
            for i in canaux:
                trame[i][t] = val_haut
            gevent.sleep(pause)
            for i in canaux:
                trame[i][t] = val_bas
            if (time.time() - tic > duree) : return 0
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
        tic = time.time()
        while (time.time() - tic < duree):
            fonction(*args)


    def boucle(self, nombre, fonction, *args):
        for i in range(0, nombre):
            fonction(*args)

    #fonction appelée régulièrement pour créer et envoyer une nouvelle trame dmx via le port série
    def send_serial(self, ard_dmx, pause):
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
            ard_dmx.write(trame_envoi)
            gevent.sleep(pause)

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
