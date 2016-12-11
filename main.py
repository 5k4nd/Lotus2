#!env/bin/python2
# -*- coding: utf8 -*-

# import socket
from threading import Thread
# from random import randint
from time import sleep
import serial  # arduino
import math
from json import loads

from pygame import mixer

# import sys
from sys import exc_info
import ast  # for str to dict cast

from dmx_functions import DMX
from effets import Effets





class daemon_sensors(Thread):
    """
        thread de l'arduino des capteurs de distance
    """
    def __init__(self, ard_sensors):
        Thread.__init__(self)
        self.arduino = ard_sensors
        self.data = {
            'capt1': 0,
            'volume': 1
        }


    def run(self):
        while 1:
            sleep(.01)
            try:
                # listen from arduino
                got = self.arduino.readline()
                got = got.replace(" ", "")  # remove blanks
                got = ast.literal_eval(got)  # cast str to dict

                # looking for the data we want
                if "axeX" in got.keys():
                    self.data['axeX'] = int(got['axeX'])
                    # self.core.logger.p_log('(axeX): ' + str(got['axeX']))
                if "capt1" in got.keys():
                    self.data['capt1'] = int(got['capt1'])
                if "capteur2var" in got.keys():
                    # insérer ici n'importe quoi :-)
                    a = 42
                if "ambiancevar" in got.keys():
                    self.data['ambiancevar'] = int(got['ambiancevar'])

            except:
                #quelle que soit l'erreur (formatage des donnees, valeurs aberrantes) on passe
                pass



class outputs_arduinos(Thread):
    """
        thread de l'arduino des sorties, pour l'instant du DMX.
    """
    def __init__(self, ref_ard_dmx, arduino_sensors):
        Thread.__init__(self)
        self.ard_dmx=ref_ard_dmx
        self.arduino_sensors=arduino_sensors
        """try:
            # mixer.init()
        except:
            print '(AUDIO) sound init error'
            print exc_info()"""

    def run(self):
        # mixer.volume = 1
        while 1:
            sleep(.01)
            try:
                # volume = self.arduino_sensors.data['volume']/200.0
                # mixer.music.set_volume(self.arduino_sensors.data['volume'])

                #distance = int(self.arduino_sensors.data['capt1'])
                #Effets.battement_de_coeur(self.ard_dmx, distance)
                effet = Effets()

                effet.sequence(ard_dmx)


            except exc_info():
                print exc_info()
                pass






if __name__ == '__main__':
    try:
        # on ouvre le port d'écoute de l'arduino MEGA
        # qui écoute les 8 ultrasons + le capteur capacitif
        ard_sensors = serial.Serial('/dev/ttyUSB0', 9600)

        # on ouvre le porte d'écoute de l'arduino DMX
        ard_dmx = serial.Serial('/dev/ttyACM1', 115200)

        # on démarre le thread d'écoute et de data processing de l'arduino MEGA
        arduino_sensors = daemon_sensors(ard_sensors)
        arduino_sensors.start()

        # on temporise le temps que le thread MEGA démarre
        sleep(1)

        # on démarre le thread qui gère l'arduino UNO DMX
        arduino_senders = outputs_arduinos(ard_dmx, arduino_sensors)
        arduino_senders.start()




    except:
        print 'problème d\'INIT'
        print exc_info()

    try:
        print ('APPUYER SUR ENTRÉE POUR QUITTER.')
        input()
    except:
        pass



    print('THE END.')
    # on arrête "proprement" les thread
    arduino_senders._Thread__stop()
    arduino_sensors._Thread__stop()
    # on ferme "proprement" les ports d'écoute des serial arduino
    ard_dmx.close()
    ard_sensors.close()
