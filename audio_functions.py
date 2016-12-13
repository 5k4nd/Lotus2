#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oui ce fichier est crade mais ça marche, et normalement vous devriez pas avoir
à mettre les mains dedans donc la flem de clener :-)
"""

from vlc import *
from time import sleep



def audio_battement(level):
    player.set_media(media)
    player.play()
    if level==1:
        sleep(.4)
    elif level==2:
        sleep(.5)
    elif level==3:
        sleep(.6)
    elif level==4:
        sleep(.7)
    elif level==5:
        sleep(.9)
    elif level==6:
        sleep(1)
    elif level==7:
        sleep(1.2)




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


filename = os.path.expanduser("data/audio/battement_punch.mp3")

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




# Some marquee examples.  Marquee requires '--sub-source marq' in the
# Instance() call above, see <http://www.videolan.org/doc/play-howto/en/ch04.html>
# player.video_set_marquee_int(VideoMarqueeOption.Enable, 1)
# player.video_set_marquee_int(VideoMarqueeOption.Size, 24)  # pixels
# player.video_set_marquee_int(VideoMarqueeOption.Position, Position.Bottom)
# if False:  # only one marquee can be specified
#     player.video_set_marquee_int(VideoMarqueeOption.Timeout, 5000)  # millisec, 0==forever
#     t = media.get_mrl()  # filename
# else:  # update marquee text periodically
#     player.video_set_marquee_int(VideoMarqueeOption.Timeout, 0)  # millisec, 0==forever
#     player.video_set_marquee_int(VideoMarqueeOption.Refresh, 1000)  # millisec (or sec?)
#     ##t = '$L / $D or $P at $T'
#     t = '%Y-%m-%d  %H:%M:%S'
# player.video_set_marquee_string(VideoMarqueeOption.Text, str_to_bytes(t))

# Some event manager examples.  Note, the callback can be any Python
# callable and does not need to be decorated.  Optionally, specify
# any number of positional and/or keyword arguments to be passed
# to the callback (in addition to the first one, an Event instance).


if __name__ == '__main__':
    sleep(1)
    while 1:
        print("new loop!")
        audio_battement(7)
        sleep(.01)
    event_manager = player.event_manager()
    event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player)



