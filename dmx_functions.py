#!env/bin/python2
# -*- coding: utf-8 -*-
import gevent
#from gevent import getcurrent
from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep
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

    def interruption(self, canaux, val):
        global interrup
        for i in canaux:
            interrup[i] = val



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

    def boucle(self, nombre, fonction, *args):
        G = []
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

