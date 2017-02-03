#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
oui ce fichier est crade mais ça marche, et normalement vous devriez pas avoir
à mettre les mains dedans donc la flem de cleaner :-)

ToDo:
- corriger le fait que j'ai actuellement une instance par fichier. c'est pratique
mais vraiment NON, ça se fait pas.

"""

from vlc import *
from time import sleep

from threading import Thread
from sys import exc_info


try:
    from msvcrt import getch
except ImportError:
    import termios
    import tty

    def getch():  # getchar(), getc(stdin)  #PYCHOK flake
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

def end_callback(event):
    print('End of media stream (event %s)' % event.type)
    sys.exit(0)

echo_position = False
def pos_callback(event, player):
    if echo_position:
        sys.stdout.write('\r%s to %.2f%% (%.2f%%)' % (event.type,
                                                      event.u.new_position * 100,
                                                      player.get_position() * 100))
        sys.stdout.flush()


### CONSTRUCTION DES INSTANCES SONORES

### le battement de coeur
filename = os.path.expanduser("data/audio/battement/battement_double2.wav")
# Need --sub-source=marq in order to use marquee below
instance = Instance(["--sub-source=marq"] + sys.argv[1:])
try:
    media = instance.media_new(filename)
except (AttributeError, NameError) as e:
    print('%s: %s (%s %s vs LibVLC %s)' % (e.__class__.__name__, e,
                                           sys.argv[0], __version__,
                                           libvlc_get_version()))
    sys.exit(1)
player = instance.media_player_new()


### séquence des sirènes
filename2 = os.path.expanduser("data/audio/sequences/2_sirenes_1222.wav")
instance2 = Instance(["--sub-source=marq"] + sys.argv[1:])
try:
    media2 = instance2.media_new(filename2)
except (AttributeError, NameError) as e:
    print('%s: %s (%s %s vs LibVLC %s)' % (e.__class__.__name__, e,
                                           sys.argv[0], __version__,
                                           libvlc_get_version()))
    sys.exit(1)
player2 = instance2.media_player_new()


### la cloche de début
filename3 = os.path.expanduser("data/audio/bell2.mp3")
instance3 = Instance(["--sub-source=marq"] + sys.argv[1:])
try:
    media3 = instance3.media_new(filename3)
except (AttributeError, NameError) as e:
    print('%s: %s (%s %s vs LibVLC %s)' % (e.__class__.__name__, e,
                                           sys.argv[0], __version__,
                                           libvlc_get_version()))
    sys.exit(1)
player3 = instance3.media_player_new()





def audio_battement(level, ref_thread_outputs_arduino):
    if ref_thread_outputs_arduino.GLOBAL_STATE_SEQUENCE:
        for i in range(100,50,-2):
            # print(i)
            # sleep(.02)
            player2.audio_set_volume(i)
            audio_stop(2)
        player2.audio_set_volume(0)
        ref_thread_outputs_arduino.GLOBAL_STATE_SEQUENCE = False
    else:
        player.audio_set_volume(100)
        player.set_media(media)
        player.play()



def audio_sequence(no, ref_thread_outputs_arduino):
    ref_thread_outputs_arduino.GLOBAL_STATE_SEQUENCE = True
    audio_stop(1)
    if no==2:
        print("début séquence 2_sirenes")
        player2.audio_set_volume(0)  # <<<< ???????? ne marche pas !!!
        player2.set_media(media2)
        player2.play()
        player2.audio_set_volume(0)



def audio_bell():
    player3.audio_set_volume(100)
    player3.set_media(media3)
    player3.play()





def audio_stop(player_no):
    """
    ToDo: rajouter la prise en charge du numéro de player.

    """
    if player_no==1:
        player.stop()
        player.audio_set_volume(0)

    if player_no==2:
        player2.stop()



if __name__ == '__main__':

    sleep(1)
    player2.set_media(media2)
    player2.play()
    # print import pprin
    print(dir(player2))
    raw_input()
    player2.audio_set_volume(0)
    raw_input()
    player2.audio_set_volume(100)
    raw_input()
    # sleep(1.2)
    # player2.set_media(media2)
    # player2.play()

    event_manager = player.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)
