#!env/bin/python2
# -*- coding: utf8 -*-

""" INFO DIVERSES

par convention nous avons choisi :
    - /dev/ttyACMO > MEGA (capteurs de distance)        à brancher en premier
    - /dev/ttyACM1 > UNO (shield DMX)                   à brancher en deuxième
    - /dev/ttyUSB0 > NANO (capteur capacitif du lotus)  à brancher en dernier


IMPORTANT :
    - au démarrage du système le capteur capacitif NE DOIT PAS ÊTRE TOUCHÉ

"""
import time

from threading import Thread
from time import sleep
import serial
import math
from json import loads

from pygame import mixer


from sys import exc_info
import ast  # for str-to-dict cast

from dmx_functions import DMX
from effets import Effets
from audio_functions import audio_bell

import time


class daemon_capacitor(Thread):
    """
        thread de l'arduino du capacitif (NANO).
        > le capacitif sur la nano du lotus se branche sur le pin 7


    """
    def __init__(self, ard_capacitor):
        Thread.__init__(self)
        self.ard_capacitor = ard_capacitor  # capteur capacitif du lotus
        self.data = {
            'capacitor_ground': -1,
            'capacitor_value': -1
        }
        self.must_start_sequence = False


    def run(self):
        """
        cette boucle tourne en boucle. peut être utile pour effectuer des
        opérations périodiques (de la transformation de données en temps-réel
            par exemple).
        elle teste notamment le CAPTEUR CAPACITIF, qui fait un front montant pendant 1 seconde lorsqu'il est touché
        """
        while 1:
            sleep(.01)
            try:
                ### LISTEN FROM ARD_CAPACITOR (capacitif Lotus)
                got = self.ard_capacitor.readline()
                got = got.replace(" ", "")  # remove blanks
                got = ast.literal_eval(got)  # cast str to dict

                if "capa" in got.keys():
                    # on ignore les 0.
                    if (int(got['capa']) == 0):
                        pass
                    else:
                        # on initialise le ground si ça n'a pas été déjà fait
                        if (self.data['capacitor_ground'] == -1):
                            self.data['capacitor_ground'] = int(got['capa'])
                            print('[INFO] ground capacitif initialisé à %s' % self.data['capacitor_ground'])

                        self.data['capacitor_value'] = int(got['capa'])
                        print self.data['capacitor_value']

                # si le capteur est touché, disons pin_ground + 5
                delta = 3
                # note : baisser delta pour plus de réactivité, l'augmenter si le lotus se déclenche tout seul ! :-)
                if (self.data['capacitor_value'] > (self.data['capacitor_ground'] + delta)):
                    #print("capacitif touché à %s" % self.data['capacitor_value'])
                    self.must_start_sequence = True
                    self.must_start_effet = True

                    # on vide le buffer
                    tic = time.time()
                    while (time.time() - tic < 1):
                        self.ard_capacitor.readline()
                else:
                    self.must_start_sequence = False
                print ("CAPACITOR %s" % self.must_start_sequence)


            except:
                #quelle que soit l'erreur (formatage des donnees, valeurs aberrantes, etc.) on passe
                pass


class arduino_ultrasonics(Thread):
    """
        thread de
            - l'arduino des capteurs de distance (MEGA)

    """
    def __init__(self, ard_sensors):
        Thread.__init__(self)
        self.ard_sensors = ard_sensors      # capteurs de ditance (ultrasonic sensors)
        self.data = {
            'capt1': 239,
        }


    def run(self):
        while 1:
            sleep(.01)
            try:

                ### LISTEN FROM ARD_SENSORS (ulrasonic sensors)
                got2 = self.ard_sensors.readline()
                got2 = got2.replace(" ", "")  # remove blanks
                got2 = ast.literal_eval(got2)  # cast str to dict

                if "capt1" in got2.keys():
                    self.data['capt1'] = int(got2['capt1'])
                if "capt2" in got2.keys():
                    self.data['capt2'] = int(got2['capt2'])


            except:
                #quelle que soit l'erreur (formatage des donnees, valeurs aberrantes) on passe
                pass



class outputs_arduinos(Thread):
    """
        thread de l'arduino des sorties, pour l'instant du DMX.
    """
    def __init__(self, ref_ard_dmx, arduino_sensors, arduino_capacitor):
        Thread.__init__(self)
        self.ard_dmx = ref_ard_dmx
        self.arduino_sensors = arduino_sensors
        self.ard_capacitor = arduino_capacitor
        """try:
            # mixer.init()
        except:
            print '(AUDIO) sound init error'
            print exc_info()"""

    def run(self):
        """
        attention cette boucle contient des opérations bloquantes. ne pas y
        placer d'opérations périodiques.
        """
        while 1:
            sleep(.01)
            effet = Effets(self.ard_dmx, self.arduino_sensors, self.ard_capacitor)

            try:
                dmx = DMX()
                effet.battement_de_coeur(dmx)

                if self.ard_capacitor.must_start_sequence:
                    effet.sequence()
                    effet.sequence_stop()


            except exc_info():
                print exc_info()
                print exc_info()[-1].tb_lineno
                pass

        # ne pas toucher, c'est pour VLC !
        event_manager = player.event_manager()
        event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
        event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)




if __name__ == '__main__':
    try:
        # on attend que le personnel de l'expo branche les trucs. on leur laisse 10 secondes À CHANGER EN 1 MINUTE !!
        #audio_bell()
        #sleep(1)

        # on ouvre le port d'écoute de l'arduino MEGA qui écoute les 8 ultrasons
        # ard_sensors = serial.Serial('/dev/ttyUSB2', 115200)
        ard_sensors = "coucou"

        # on démarre le thread d'écoute et de data processing de l'arduino MEGA
        arduino_sensors = arduino_ultrasonics(ard_sensors)
        arduino_sensors.start()


        # on ouvre le port d'écoute de l'arduino NANO qui écoute le lotus
        ard_capacitor = serial.Serial('/dev/ttyACM0', 115200)
        # ard_capacitor = "coucou"

        # on démarre le thread d'écoute et de data processing de l'arduino NANO
        arduino_capacitor = daemon_capacitor(ard_capacitor)
        arduino_capacitor.start()



        # on temporise le temps que le thread MEGA démarre et recoive ses premières données
        sleep(1)

        # on ouvre le port d'écoute de l'arduino UNO-DMX
        ard_dmx = serial.Serial('/dev/ttyACM1', 115200)
        #ard_dmx = "coucou"

        # on démarre le thread qui gère l'arduino UNO DMX
        arduino_senders = outputs_arduinos(ard_dmx, arduino_sensors, arduino_capacitor)
        arduino_senders.start()

    except:
        print 'problème d\'INIT'
        print exc_info()
        print exc_info()[-1].tb_lineno
        pass




    try:
        print ('APPUYER SUR ENTRÉE POUR QUITTER.')
        input()
    except:
        pass



    print('THE END.')
    # on arrête "proprement" les thread
    arduino_senders._Thread__stop()
    arduino_capacitor._Thread__stop()
    arduino_sensors._Thread__stop()
    # on ferme "proprement" les ports d'écoute des serial arduino
    ard_dmx.close()
    ard_capacitor.close()
    ard_sensors.close()
