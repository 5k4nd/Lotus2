#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dmx_functions import DMX
import gevent
#from gevent import getcurrent
from gevent.pool import Group

class Effets():
    """
        dans cette classe se trouvent tous les effets.
        généralement un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son
    """
    def __init__(self, ard_dmx, ard_sensors):
        self.dmx = DMX()
        self.ard_dmx = ard_dmx
        self.ard_sensors = ard_sensors
        


    def sequence(self):
        dmx = self.dmx
        while 1:
            g1 = gevent.spawn(dmx.fade_up_down, 2, 0.1, 0, 255)
            g2 = gevent.spawn(dmx.fade_up_down, 3, 0.1, 0, 255)
            g3 = gevent.spawn(dmx.fade_up_down, 4, 0.1, 0, 255)
            g4 = gevent.spawn(dmx.send_serial, self.ard_dmx, 0.03)
            gevent.joinall([g1, g2, g3])
            g4.kill()

    def battement_de_coeur(self):
        distance = self.ard_sensors.data['capt1']  # remplacer par un truc pertinent !
        if distance < 50:
            print("battement 3")
            # mixer.music.load("data/audio/heartbeat_solo_3.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(self.ard_dmx, 0, 150, 8)
            sleep(.3)
            # mixer.music.stop()

        elif ((distance >= 50) & (distance < 100)):
            print("battement 2")
            # mixer.music.load("data/audio/heartbeat_solo_2.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(self.ard_dmx, 0, 150, 6)
            SON.battement()
            sleep(.7)
            # mixer.music.stop()
        elif distance >= 100:
            print("battement 1")
            # mixer.music.load("data/audio/heartbeat_solo_1.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(self.ard_dmx, 0, 150, 3)
            sleep(1.2)
            # mixer.music.stop()
