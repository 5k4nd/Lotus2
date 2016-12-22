#!env/bin/python2
# -*- coding: utf-8 -*-
import gevent
#from gevent import getcurrent
from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep
from math import *

trame = [0]*20


class DMX():

    #battement linéaire (limité en fréquence à 0.1s environ)
    def zero(self):
        for i in range(1,len(trame)):
            trame[i] = 0

    def fade_up_down(self, canal, duree, val_dep, val_fin, pas):
        global trame
        pause = (float(duree)/abs(val_dep-val_fin))*float((pas/2))
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        for i in valeurs:
            trame[canal] =  i
            gevent.sleep(pause)
        for i in reversed(valeurs):
            trame[canal] =  i
            gevent.sleep(pause)

    def fade(self, canal, duree, val_dep, val_fin, pas):
        global trame
        pause = (float(duree)/abs(val_dep-val_fin))*pas
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -pas)
        else : valeurs = range(val_dep, val_fin, pas)
        for i in valeurs:
            if i<=pas :
                i=0
            trame[canal] =  i
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
        while 1:
            global trame
            nb_canaux = len(trame)
            trame_envoi = ""
            for i in range(1, nb_canaux):
                trame_envoi = trame_envoi + str(i) + "c" + str(trame[i]) + "w"
            ard_dmx.write(trame_envoi)
            gevent.sleep(pause)

    def battement(ard_dmx, BEGIN, END, PAS=1):
        for i in range(BEGIN, END, PAS):
            sleep(.008)
            ard_dmx.write("D"+str(i)+",0,0")
            # print i
        for i in range(END-1, BEGIN-1, -1*PAS):
            sleep(.008)
            if i < PAS:
                break  # sécurité quand le pas ne permet pas d'arriver sur un beau 0
            ard_dmx.write("D"+str(i)+",0,0")
            # print i
        print ("ok")
        ard_dmx.write("D"+str(BEGIN)+",0,0")
        ard_dmx.write("D"+str(BEGIN)+",0,0")
