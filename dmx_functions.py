#!env/bin/python2
# -*- coding: utf-8 -*-


# DMX functions
def fade_up_green():
    for i in range(0, 255):
        ard_dmx.write("D0,"+str(i)+",0")
        print i
        sleep(.01)
    for i in range(255, -1, -1):
        ard_dmx.write("D0,"+str(i)+",0")
        print i
        sleep(.01)
    ard_dmx.write("D0,0,0")

def fade_up_red():
    for i in range(0, 255):
        ard_dmx.write("D"+str(i)+",0,0")
        print i
        sleep(.01)
    for i in range(255, -1, -1):
        ard_dmx.write("D"+str(i)+",0,0")
        print i
        sleep(.01)
    ard_dmx.write("D0,0,0")
    ard_dmx.write("D0,0,0")

def battement(BEGIN, END, PAS=1):
    for i in range(BEGIN, END, PAS):
        sleep(.008)
        ard_dmx.write("D"+str(i)+",0,0")
        # print i
    for i in range(END-1, BEGIN-1, -1*PAS):
        sleep(.008)
        if i < PAS:
            break  # sécurité quand le pas ne permet pas d'arriver sur un beau 0
        ard_dmx.write("D"+str(i)+",0,0")
        # print i
    print ("ok")
    ard_dmx.write("D"+str(BEGIN)+",0,0")
    ard_dmx.write("D"+str(BEGIN)+",0,0")
