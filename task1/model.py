# -*- coding: utf-8 -*-

'''
Created on Oct 7, 2013

@author: yuankunluo

'''
import re
import time

class Sentence:
    textInfo = []
    cnInfo = []
    linInfo = []
    tagInfo = []
    posInfo = []
    enInfo = []
    id = ''
    clusters = []
    preSent = None
    nextSent = None

    def __repr__(self):
        if self is None:
            return ''
        sent = "{s}\n"
        sent += "ID: " + self.id + "\n"
        if(len(self.enInfo) > 0):
            sent += "CN: " + " ".join(self.cnInfo) + "\n"
            sent += "EN: " + " ".join(self.enInfo) + "\n"
        else:
            sent += "TEXT: " + ' '.join(self.textInfo) + "\n"
        sent += "POS: " + " ".join(self.posInfo) + "\n"
        sent += "TAG: " + " ".join(self.tagInfo) + "\n"
        sent += "{s}"
        return sent.format(s="-"*20)

    def __str__(self):
        if self is None:
            return ''
        sent = "{s}\n"
        sent += "ID: \t" + self.id.decode() + "\n"
        if(len(self.enInfo) > 0):
            sent += "CN: \t" + " ".join(self.uniToPrint(self.cnInfo)) + "\n"
            sent += "EN: \t" + " ".join(self.uniToPrint(self.enInfo)) + "\n"
        else:
            sent += "TEXT: \t" + ' '.join(self.uniToPrint(self.textInfo)) + "\n"
        sent += "POS: \t" + " ".join(self.uniToPrint(self.posInfo)) + "\n"
        sent += "TAG: \t" + " ".join(self.uniToPrint(self.tagInfo)) + "\n"
        sent += "{s}"
        return sent.format(s = "-"*20)
    
    def uniToPrint(self, info = []):
        results = []
        if len( info ) > 0:
            for cp in info:
                results.append(cp.decode())
        else:
            return None
        return results

    def makeClusters(self):
        results = []
        
        


class Cluster:
    c_id = ''
    pinInfo = []
    cnInfo = []
    tagInfo = []
    posInfo = []
    preCluster = None
    nextCluster = None

    pass

class Corpus:
    """
    Corpus has a content perporty to store every section,
    like A:{}
    """
    name = ""
    created_time = None
    contentsList = []
    contentsDict = {}
    sections = []

    def __init__(self, name=None):
        if name is None:
            name = "Default Unnamed Corpus"
        self.name = name
        self.created_time = time.ctime()
        self.contents = {}

    def getSections(self):
        sc = ",".join([str(i) for (i, t) in self.sections])
        return sc

    def getVolume(self):
        volume = (len(self.contentsList))
        return str(volume)


    def __repr__(self):
        text = "{s}\nCorpus Information:\n"
        text += "\tCorpus Name: {name}\n"
        text += "\tCreated Time: {time}\n"
        text += "\tSections Numbers: " + self.getSections() + "\n"
        text += "\tCorpus Volume: " + self.getVolume() + "\n"
        text += "{s}"
        return text.format(s="="*20, name=self.name, time=self.created_time)

    def getSentByID(self, ID):
        try:
            sent = self.contentsDict.get(ID)
            if sent != None:
                return sent
        except:
            print("KeyError:%s. Not Fund in Corpus." % (ID))

    def getSentsByRange(self, first, last):
        if isinstance(first, int) and isinstance(last, int):
            try:
                results = self.contentsList[first:last]
                return results
            except:
                print("RangeError: %s - %s not valid." % (str(first), str(last)))
        else:
            print("Please give a range with int.")

class Task:
    name = ""
    desc = ""
    cnPattern = None
    enPattern = None
    result = None
    
    def __init__(self, taskName, taskDesc, cnPattern = None,
                 enPattern = None):
        if len(taskName) >= 0:
            if isinstance(taskName, str):
                taskName = unicode(taskName)
            if isinstance(taskName, unicode):
                self.name = taskName
        else:
            self.name = unicode("Unknown Task")
        if len(taskDesc) >= 0:
            if isinstance(taskDesc, str):
                self.desc = unicode(taskDesc)
            if isinstance(taskDesc, unicode):
                self.desc = taskDesc
            if isinstance(taskDesc, list):
                self.desc = ','.join(taskDesc)
        else:
            self.desc = unicode("Unknown task description.")
        self.cnPattern = cnPattern
        self.enPattern = enPattern
    
    def __str__(self):
        result = "{s}"
        result += self.name.decode() + "\n"
        result += self.desc.decode() + "\n"
        result += "{s}"
        return result.format(s = "+"*40+"\n")
        







