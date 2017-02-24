#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
oui ce fichier est crade mais ça marche, et normalement vous devriez pas avoir
à mettre les mains dedans donc la flem de cleaner :-)

ToDo:
    - corriger le fait que j'ai actuellement une instance par fichier. c'est pratique
        mais franchement : NON, ça se fait pas !

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
player_battement = instance.media_player_new()


def audio_battement(level, ref_thread_events):
    print("AUDIO: début BATTEMENT")
    ## si on arrive de la séquence on fait une transition en douceur :-)
    player4.stop()
    if ref_thread_events.state['sequence']:
        for i in range(100,50,-2):
            # print(i)
            # sleep(.02)
            player2.audio_set_volume(i)
            audio_stop(2)
        player2.audio_set_volume(0)
        ref_thread_events.state['sequence'] = False
    # elif ref_thread_events.state['intro']:
    #     ref_thread_events.state['intro'] = False
    else:
        player_battement.audio_set_volume(100)
        player_battement.set_media(media)
        player_battement.play()




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


def audio_sequence(ref_thread_events):
    # audio_stop()
        
    ref_thread_events.state['sequence'] = True
    print("AUDIO: début SEQUENCE")
    # player.audio_set_volume(0)  # <<<< ???????? ne marche pas !!!
    player2.stop()
    player2.set_media(media2)
    player2.play()
    player2.audio_set_volume(0)




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



def audio_bell():
    player3.audio_set_volume(100)
    player3.set_media(media3)
    player3.play()




### sequence initiale
filename4 = os.path.expanduser("/media/media/Abelum/Lotus/code/data/audio/intro/Those_Were_Good_Times.mp3")
instance4 = Instance(["--sub-source=marq"] + sys.argv[1:])
try:
    media4 = instance4.media_new(filename4)
except (AttributeError, NameError) as e:
    print('%s: %s (%s %s vs LibVLC %s)' % (e.__class__.__name__, e,
                                           sys.argv[0], __version__,
                                           libvlc_get_version()))
    sys.exit(1)
player4 = instance4.media_player_new()



def audio_intro(ref_thread_events):
    print("AUDIO: début séquence CAVERNE")
    player4.audio_set_volume(50)
    player4.set_media(media4)
    player4.play()








def audio_stop(var):
    if var=="sequence":
        player2.stop()

    else:
        player_battement.stop()
        player_battement.audio_set_volume(0)



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

    # event_manager = player_battement.event_manager()
    # event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    # event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player_battement)
