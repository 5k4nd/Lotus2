#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Effets():
    """
        dans cette classe se trouvent tous les effets.
        généralement un effet gère ensuite deux types de sous-effets :
            - les effets lumières via la classe DMX (importée depuis dmx_functions)
            - les effets de son
    """
    def sequence

    def battement_de_coeur(ard_dmx, distance):
        if distance < 50:
            print("battement 3")
            # mixer.music.load("data/audio/heartbeat_solo_3.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(ard_dmx, 0, 150, 8)
            sleep(.3)
            # mixer.music.stop()

        elif ((distance >= 50) & (distance < 100)):
            print("battement 2")
            # mixer.music.load("data/audio/heartbeat_solo_2.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(ard_dmx, 0, 150, 6)
            SON.battement()
            sleep(.7)
            # mixer.music.stop()
        elif distance >= 100:
            print("battement 1")
            # mixer.music.load("data/audio/heartbeat_solo_1.mp3")
            # mixer.music.play()
            sleep(.3)
            DMX.battement(ard_dmx, 0, 150, 3)
            sleep(1.2)
            # mixer.music.stop()
