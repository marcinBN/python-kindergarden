#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import sys
import json
import time
import Queue
import select
import optparse
import threading
from autopy import *

# better user interface would be recommended

# usage example:
# python bot.py action record baba.json
# i enter
# gotoxy 23 43
# i enter
# typestring teststring
# 3
# e enter
#
# python bot.py action read baba.json


def parse_args():
    usage = """usage: %prog [option] arg"""
    parser = optparse.OptionParser(usage)
    parser.add_option('-a', '--action', help='record / read filename')
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.error('Provide exactly one filename')

    filename = args[0]
    option = options.action

    if option not in ['record', 'read']:
        parser.error('No such option: %s' % option)
    
    if option == 'read' and not os.path.exists(filename):
        parser.error('No such file: %s' % filename)

    return option, filename

def gotoxy(x, y):
    print 'final step'
    autopy.mouse.smooth_move(x, y)

def clickleft():
    mouse.click(mouse.LEFT_BUTTON)

def clickright():
    mouse.click(mouse.RIGHT_BUTTON)

def showCoords():
    print mouse.get_pos()

def typestring(s, wpm=15):
    key.type_string(s, wpm)

def saveToJSON(filename, data):
    data = json.dumps(data)
    with open(filename, 'w') as f:
        f.write(data)

def loadFromJSON(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def recordAction(filename):
    print 'Enter steps:'
    steps = []
    timeout = 0
    read_list = [sys.stdin]
    line = ''
    while read_list:
        ready = select.select(read_list, [], [], timeout)[0]
        if not ready:
            showCoords()
        else:
            for file in ready:
                line = file.readline()
                if not line:
                    read_list.remove(file)
                else: 
                    line = line.rstrip()
                    if line == 'e':
                        saveToJSON(filename, steps)
                        sys.exit()
                    elif line == 'i':
                        comm = raw_input('>')
                        steps.append(comm.split())

    
    #saveToJSON(filename, [['gotoxy', 5, 5], ['gotoxy', 300, 300], ['clickleft'], ['typestring', 'marcin'], 3])

        

def performAction(filename):
    steps = loadFromJSON(filename)
    last = len(steps)-1
    repetitions = int(steps[last][0])
    for j in range(repetitions):
        for i in range(last):
            step = steps[i]
            command = step[0]
            print 'command=', repr(command)
            if command == 'gotoxy':
                x = int(step[1])
                y = int(step[2])
                print 'step 1'
                gotoxy(x, y)
            elif command == 'typestring':
                s = step[1]
                typestring(s)
            elif command == 'clickleft':
                clickleft()
            elif command == 'clickright':
                clickright()


    

if __name__ == '__main__':
    option, filename = parse_args()
    if option == 'record':
        try:
            recordAction(filename)
        except KeyboardInterrupt:
            pass

    elif option == 'read':
        performAction(filename)




