"""
XML parsing:  ElementTree
"""
import os
os.chdir('C:/Users/Yk.LUO/Desktop/lilei/programm')

from xml.etree.ElementTree import parse
sDir =r'C:\Users\Yk.LUO\Desktop\lilei\Corpus\LCMC\standard'
sDir = sDir.replace('\\','/')
mapping = {}

