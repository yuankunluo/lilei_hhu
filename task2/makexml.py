# -*- coding: utf-8 -*-

import os
import re

s = "　　在金町车站下车时，又是一番辛苦。亲身体会他才深深觉得，公共交通工具不应该只设计“博爱座”，而应该为老年人、残障者特制专用的车厢才对。这么一来，上下车的时候他们可以不必担心跟其他乘客碰撞。这种车厢的开关门速度也要慢一点，让乘客不必慌张。"

def readText(inputfile = "../input/huoche.txt"):
    lines_raw = []
    with open(inputfile) as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                lines_raw.append(line)
    return lines_raw
    
                
def cleanLines(rawLines):
    result = []
    for line in rawLines:
        sentens = processLine(line)
    return result
    
def processLine(inputLine):
    puctation = ["，","。","" ]

        
rawLines = readText()
cleanLines = cleanLines(rawLines)        
        
    