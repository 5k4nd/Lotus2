#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
oui ce fichier est crade mais ça marche, et normalement vous devriez pas avoir
à mettre les mains dedans donc la flem de cleaner :-)
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




def audio_battement(level):
    player.set_media(media)
    player.play()

def audio_sequence(no):
    if no==2:
        player2.set_media(media2)
        player2.play()

def audio_stop(player_no):
    player2.stop()

if __name__ == '__main__':
    sleep(1)
    # while 1:
    try:
        player2.set_media(media2)
        player2.play()
    except:
        print exc_info()
    # sleep(1.2)
    # player2.set_media(media2)
    # player2.play()

    event_manager = player.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)



