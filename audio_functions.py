#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Le principe de ce module est simple.
1) On crée une instance VLC : instance.
2) On crée un lecteur de média vlc : player. Il contient notammement les
    contrôles de volume, le périphérique audio, etc.
3) On crée un lecteur de liste de lecture : media_player. Il contient les
    médias et les contrôle start, pause, loop, etc.
4) On link player et media_player.

Remarque : je concède que dissocier le media_player et le mediaplayer n''est
pas hyper intuitif mais c'est un choix des gars de chez VLC. ;-)


ATTENTION, l'api vlc gère mal la fin d'un stream par défaut (génère des
    exceptions non gérées). moi je m'en sors en répétant éternellement ma liste
    de lecture mais soyez prudents.


Bapt, mars 2017.

"""

from vlc import *
from time import sleep


def fade_volume(start, end):
    if start<end:
        pas =1
    else:
        pas =-1
    for i in range(start, end, pas):
            sleep(.001)
            player.audio_set_volume(i)

def audio_init(medias):
    # on crée l'instance vlc. elle peut et devrait être singleton !
    instance = Instance(medias)
    player = instance.media_player_new()

    medialist = instance.media_list_new()
    for media in medias: 
        medialist.add_media(instance.media_new(media))

    media_player = instance.media_list_player_new()
    media_player.set_media_player(player)
    media_player.set_media_list(medialist)

    return player, media_player


def start_intro_first_time(player, media_player):
    """
        au lancement de l'appli, lors de la première boucle.
    """
    player.audio_set_volume(30)
    media_player.play()

    # attention, doit être appelée après le play(), wouais c'est bizarre :/
    media_player.set_playback_mode(PlaybackMode.repeat)


def start_battement(player, media_player):
    # attention, on ne doit plus boucler pour passer au battement
    media_player.set_playback_mode(PlaybackMode.default)

    # on baisse le volume
    
    fade_volume(30, 0)
    media_player.next()
    fade_volume(0, 150)

    # on boucle à nouveau, sur le battement
    media_player.set_playback_mode(PlaybackMode.repeat)


def start_sequence(player, media_player):
    # pour reboucler sur l'intro à la fin de la séquence
    media_player.set_playback_mode(PlaybackMode.default)

    fade_volume(150, 0)
    media_player.next()
    fade_volume(0, 50)
    print("AUDIO: fin sequence")


def start_intro_loop(player, media_player):
    """
        lorsque l'intro se lance après une première exécution complète du programme,
        donc après la séquence.
    """
    ## on loope, pour repartir vers l'INTRO
    media_player.set_playback_mode(PlaybackMode.loop)
    fade_volume(50, 0)
    media_player.next()
    fade_volume(0, 30)



if __name__ == '__main__':
    medias = [
        os.path.expanduser("data/audio/intro/Those_Were_Good_Times.mp3"),
        os.path.expanduser("data/audio/intro/lotus_battement.wav"),
        os.path.expanduser("data/audio/sequences/2_sirenes_170102.wav"),
    ]

    player, media_player = audio_init(medias)

    start_intro_first_time(player, media_player)
    sleep(3)
    while 1:
        start_battement(player, media_player)
        sleep(1)

        start_sequence(player, media_player)
        sleep(4)

        start_intro_loop(player, media_player)
        sleep(3)

    # event_manager = player_battement.event_manager()
    # event_manager.event_attach(EventType.MediaPlayerEndReached,      end_callback)
    # event_manager.event_attach(EventType.MediaPlayerPositionChanged, pos_callback, player_battement)