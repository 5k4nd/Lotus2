#!env/bin/python2
# -*- coding: utf-8 -*-
import gevent
#from gevent import getcurrent
from gevent.pool import Group
from gevent.event import AsyncResult
from time import sleep
from math import *
trame = [0]*5
# DMX functions
class DMX():

    #battement linéaire (limité en fréquence à 0.1s environ)
    def fade_up_down(self, canal, duree, val_dep, val_fin):
        global trame
        pause = (float(duree)/float(abs(val_dep-val_fin)))/2
        if val_dep > val_fin :
            valeurs = range(val_dep,val_fin, -1)
        else : valeurs = range(val_dep, val_fin)
        for i in valeurs:
            #ard_dmx.write(str(canal)+"c"+str(i)+"w")
            trame[canal] =  i
            gevent.sleep(pause)
        for i in reversed(valeurs):
            #ard_dmx.write(str(canal)+"c"+str(i)+"w")
            trame[canal] =  i
            gevent.sleep(pause)

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


    def fade_up_green(ard_dmx):
        for i in range(0, 255):
            ard_dmx.write("D0,"+str(i)+",0")
            print i
            sleep(.01)
        for i in range(255, -1, -1):
            ard_dmx.write("D0,"+str(i)+",0")
            print i
            sleep(.01)
        ard_dmx.write("D0,0,0")

    def fade_up_red(ard_dmx):
        for i in range(0, 255):
            ard_dmx.write("D"+str(i)+",0,0")
            print i
            sleep(.01)
        for i in range(255, -1, -1):
            ard_dmx.write("D"+str(i)+",0,0")
            print i
            sleep(.01)
        ard_dmx.write("D0,0,0")
        ard_dmx.write("D0,0,0")

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
