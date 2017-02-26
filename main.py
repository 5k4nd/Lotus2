#!env/bin/python2
# -*- coding: utf8 -*-

"""

==== ports usb (convention de branchement) ====
EMPTY            > 3-1                3-9  < UNO_DMXO
MEGA_ULTRASONICS > 3-2                3-10 < MEGA_CAPACITOR



IMPORTANT :
    - au démarrage du système le capteur capacitif NE DOIT PAS ÊTRE TOUCHÉ



ToDo:
    - ULTRASONICS: faire un algo de traitement et de fiabilisation de la donnée de distance (redondance, moyenne, valeurs aberrantes ?)
    - SCÉNO: éclairer le lotus de telle sorte que ça fasse des ombres
"""

############################### config ########################################
UNO_DMX             = "/dev/ttyACM0"    # shield DMX                        à brancher en premier
MEGA_ULTRASONICS    = "/dev/ttyACM1"    # capteurs de distance              à brancher en deuxième
MEGA_CAPACITOR      = "/dev/ttyUSB0"    # capacitif branché sur le lotus    à brancher en troisième


###############################################################################


import serial
import ast  # pour les cast de str vers dict

from threading import Thread
from time import sleep, time
from sys import exc_info

from dmx_functions import DMX
from effets import Effets
from audio_functions import audio_bell, audio_stop


# import math
# from json import loads
# import time
# from pygame import mixer



class Thread_Lotus(Thread):
    """
        thread de l'arduino MEGA du capacitif branché sur le lotus
            > le capacitif sur la mega du lotus se branche sur le pin PWM 8


    """
    def __init__(self, arduino_lotus):
        Thread.__init__(self)
        self.arduino_lotus = arduino_lotus
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
                ## on écoute le capacitif du lotus
                got_lotus = self.arduino_lotus.readline()
                got_lotus = got_lotus.replace(" ", "")   # remove blanks
                got_lotus = ast.literal_eval(got_lotus)  # cast str to dict
                

                if "capa" in got_lotus.keys():
                    # on ignore les 0
                    if (int(got_lotus['capa']) == 0):
                        pass
                    else:
                        # on initialise le ground si ça n'a pas été déjà fait
                        if (self.data['capacitor_ground'] == -1):
                            self.data['capacitor_ground'] = int(got_lotus['capa'])
                            print('[INFO] ground capacitif initialisé à %s' % self.data['capacitor_ground'])

                        self.data['capacitor_value'] = int(got_lotus['capa'])
                        # print self.data['capacitor_value']

                # si le capteur est touché, càd valeur ded pin_ground + delta
                delta = 2
                # note : baisser delta pour plus de réactivité, l'augmenter si le lotus se déclenche tout seul ! :-)
                if (self.data['capacitor_value'] > (self.data['capacitor_ground'] + delta)):
                    print("capacitif touché à %s" % self.data['capacitor_value'])
                    self.must_start_sequence = True
                    self.must_start_effet = True

                    # on vide le buffer
                    tic = time()
                    while (time() - tic < 1):
                        self.arduino_lotus.readline()
                else:
                    self.must_start_sequence = False


            except:
                # quelle que soit l'erreur (formatage des donnees, valeurs aberrantes, etc.) on passe
                pass


class Thread_Ultrasonics(Thread):
    """
        thread de l'arduino des capteurs de distance (MEGA)

        actuellement je n'utilise qu'un capteur sur deux et je base tout dessus.

    """
    def __init__(self, arduino_ultrasonics):
        Thread.__init__(self)
        self.arduino_ultrasonics = arduino_ultrasonics
        self.data = {
            'standard_distance': 120,   # on considère que le mur face aux capteurs est à 1 mètre
            'capt1': [120]*4,           # on stocke sur la durée pour résister aux fluctuations d'erreurs électriques
        }
        self.visitors_detected = False


    def run(self):
        while 1:
            sleep(.001)
            try:
                got_ultrasonics = self.arduino_ultrasonics.readline()
                got_ultrasonics = got_ultrasonics.replace(" ", "")  # remove blanks
                got_ultrasonics = ast.literal_eval(got_ultrasonics)  # cast str to dict


                if "capt1" in got_ultrasonics.keys():
                    self.data['capt1'].pop()
                    tmp = int(got_ultrasonics['capt1'])
                    self.data['capt1'].insert(0, tmp)
                    # print tmp

                distance_delta = 20

                if (tmp < self.data['standard_distance'] - distance_delta):
                    print("MAIN: variation capteurs de distance %s centimètres" % tmp)

                # on teste toutes les dernières valeurs pour décider de la présence de gens ou non
                if all(
                    item < ( (self.data['standard_distance'] - distance_delta) )
                    for
                        item
                    in
                        self.data['capt1']):
                    print("VISITORS DETECTED")
                    self.visitors_detected = True



                # if "capt2" in got_ultrasonics.keys():
                #     self.data['capt2'] = int(got_ultrasonics['capt2'])


            except:
                #quelle que soit l'erreur (formatage des donnees, valeurs aberrantes) on passe
                pass



class Thread_Events(Thread):
    """
        thread qui gère le déclenchement des évènements de la classe EFFETS.

        Note : le lotus doit être agressé (battements de coeur) pour lancer la séquence.
    """

    def __init__(self, ref_arduino_dmx, thread_ultrasonics, thread_lotus):
        Thread.__init__(self)
        self.arduino_dmx = ref_arduino_dmx
        self.thread_ultrasonics = thread_ultrasonics
        self.thread_lotus = thread_lotus

        # la variable self.state['sequence'] est nécessaire dans audio_functions.py pour baisser proprement le volume si on sort de la séquence inopinément
        # par exemple si le lighteux te fait finir la séquence alors que la musique est pas finie (sic).
        # voir la méthode audio_battement() pour plus de détails
        self.state = {
            'intro': True,
            'battement': False,
            'sequence': False
        }
        self.dmx = DMX()
        self.effets = Effets(self.arduino_dmx, self.thread_ultrasonics, self.thread_lotus)


    def run(self):
        """
            ATTENTION cette boucle contient des opérations bloquantes
            DONC attention ne pas y placer d'opérations périodiques !
        """
        while 1:
            sleep(.01)

            try:
                ## BATTEMENT
                if self.thread_ultrasonics.visitors_detected or self.state['battement']:
                # if 0 or self.state['battement']:
                    self.state['battement'] = True
                    self.state['intro'] = False
                    print("MAIN: start battement")
                    self.effets.battement_de_coeur(self.dmx, ref_thread_events=self)
                
                    ## SEQUENCE
                    if self.thread_lotus.must_start_sequence:
                        self.state['battement'] = False
                        self.state['sequence'] = True
                        print("MAIN: start sequence")
                        self.effets.sequence(ref_thread_events=self)

                        print("MAIN: on reset le visitors_detected à FALSE")
                        self.thread_ultrasonics.visitors_detected = False
                        audio_stop("sequence")

                else:
                    ## INTRO
                    print("MAIN: start intro")
                    self.effets.sequence_intro_caverne(self.dmx, ref_thread_events=self)



            except exc_info():
                print exc_info()
                print exc_info()[-1].tb_lineno
                pass




if __name__ == '__main__':
    try:
        # signal spécifiant que le système est démarré et sera opérationnel d'ici quelques secondes
        # audio_bell()
        # sleep(1)

        # on ouvre le port d'écoute de l'arduino MEGA qui écoute les 2 ultrasons de détection de passage
        arduino_ultrasonics = serial.Serial(MEGA_ULTRASONICS, 115200)
        # arduino_ultrasonics = "foobar"

        # on démarre le thread associé
        thread_ultrasonics = Thread_Ultrasonics(arduino_ultrasonics)
        thread_ultrasonics.start()


        # on ouvre le port d'écoute de l'arduino MEGA qui écoute le lotus
        arduino_lotus = serial.Serial(MEGA_CAPACITOR, 115200)
        # arduino_lotus = "foobar"

        # on démarre le thread associé
        thread_lotus = Thread_Lotus(arduino_lotus)
        thread_lotus.start()



        # on temporise le temps que les threads démarrent et recoivent leurs premières données
        sleep(1)

        # on ouvre le port d'écoute de l'arduino UNO-DMX
        arduino_dmx = serial.Serial(UNO_DMX, 115200)
        # arduino_dmx = "foobar"

        # on démarre le thread associé
        try:
            thread_events = Thread_Events(arduino_dmx, thread_ultrasonics, thread_lotus)
            thread_events.start()
        except:
            print("MAIN: impossibles de démarrer l'Arduino DMX")

    except:
        print 'MAIN: problème d\'INIT des threads'
        print exc_info()
        print exc_info()[-1].tb_lineno
        pass


    try:
        print ('APPUYER SUR ENTRÉE POUR QUITTER.')
        input()
    except:
        pass



    # on arrête "proprement" les threads
    thread_events._Thread__stop()
    thread_lotus._Thread__stop()
    thread_ultrasonics._Thread__stop()
    
    # on ferme "proprement" les ports d'écoute des serial arduino
    arduino_dmx.close()
    arduino_lotus.close()
    arduino_ultrasonics.close()
    
    print('THE END.')
