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

from dmx_functions import *







class daemon_sensors(Thread):
    """
        thread de l'arduino des capteurs de distance
    """
    def __init__(self, port, baud):
        Thread.__init__(self)
        self.arduino = serial.Serial(port=port, baudrate=baud)
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
        try:
            mixer.init()
        except:
            print '(AUDIO) sound init error'
            print exc_info()

    def run(self):
        mixer.volume = 1    
        while 1:
            sleep(.01)
            try:
                # volume = self.arduino_sensors.data['volume']/200.0
                # mixer.music.set_volume(self.arduino_sensors.data['volume'])

                distance = int(self.arduino_sensors.data['capt1'])
                # distance = 30
                print distance

                if distance < 50:
                    print("battement 3")
                    mixer.music.load("data/audio/heartbeat_solo_3.mp3")
                    mixer.music.play()
                    sleep(.3)
                    battement(self.ard_dmx, 0, 150, 8)
                    sleep(.3)
                    mixer.music.stop()

                elif ((distance >= 50) & (distance < 100)):
                    print("battement 2")
                    mixer.music.load("data/audio/heartbeat_solo_2.mp3")
                    mixer.music.play()
                    sleep(.3)
                    battement(self.ard_dmx, 0, 150, 6)
                    sleep(.7)
                    mixer.music.stop()
                elif distance >= 100:
                    print("battement 1")
                    mixer.music.load("data/audio/heartbeat_solo_1.mp3")
                    mixer.music.play()
                    sleep(.3)
                    battement(self.ard_dmx, 0, 150, 3)
                    sleep(1.2)
                    mixer.music.stop()

                # print color
                # self.ard_dmx.write("D"+str(0)+","+str(int(color))+","+str(0))

            except exc_info():
                print exc_info()
                pass






if __name__ == '__main__':
    try:
        ard_dmx = serial.Serial('/dev/ttyACM0', 115200)

        arduino_sensors = daemon_sensors('/dev/ttyUSB0', 115200)
        arduino_sensors.start()

        sleep(1)
        arduino_senders = outputs_arduinos(ard_dmx, arduino_sensors)
        arduino_senders.start()




    except:
        print 'problème d\'INIT'
        print exc_info()

    try:
        # ard_dmx.write("D255,0,0")
        sleep(2)
        input()
    except:
        pass



    print('THE END.')
    arduino_sensors._Thread__stop()
    arduino_senders._Thread__stop()
    