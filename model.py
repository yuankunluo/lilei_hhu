# -*- coding: utf-8 -*-

'''
Created on Oct 7, 2013

@author: yuankunluo

'''
import re
import time

def uniToPrint(info = []):
    results = []
    if len( info ) > 0:
        for cp in info:
            results.append(cp.decode())
    else:
        return None
    return results


class Sentence:
    textInfo = []
    cnInfo = []
    linInfo = []
    tagInfo = []
    posInfo = []
    enInfo = []
    ID = ''
    clusters = []
    preSent = None
    nextSent = None
    
    def __init__(self):
        pass
    
    def __init__(self, ID = 0, cnInfo = None, enInfo = None, posInfo = None, tagInfo = None,):
        self.ID = ID
        self.cnInfo = cnInfo
        self.enInfo = enInfo
        self.tagInfo = tagInfo
        self.posInfo = posInfo
    
    
    def htmlPrint(self):
        pass
            
            
    
    def htmlOutput(self):
        pass

    def __repr__(self):
        if self is None:
            return ''
        sent = "{s}\n"
        sent += "ID: " + self.ID + "\n"
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
        sent += "ID: \t" + self.ID.decode() + "\n"
        if(len(self.enInfo) > 0):
            sent += "CN: \t" + " ".join(uniToPrint(self.cnInfo)) + "\n"
            sent += "EN: \t" + " ".join(uniToPrint(self.enInfo)) + "\n"
        else:
            sent += "TEXT: \t" + ' '.join(uniToPrint(self.textInfo)) + "\n"
        sent += "POS: \t" + " ".join(uniToPrint(self.posInfo)) + "\n"
        sent += "TAG: \t" + " ".join(uniToPrint(self.tagInfo)) + "\n"
        sent += "Clusters: \t" + str(len(self.clusters)) + "\n"
        sent += "{s}"
        return sent.format(s = "-"*20)
    

    def makeClusters(self):
        results = []
        # the list of punctuation in chinese
        punctuation = [u"。" , u"，",u"！",u"——",u"；",u"：",u"？"]
        start = 0
        end = 0
        IDbase = 0
        for index in range(len(self.cnInfo)):
            if self.cnInfo[index] in punctuation:
                end = index
                ID = self.ID + ":" + str(IDbase)
                cnInfo = self.cnInfo[start : end]
                enInfo = self.enInfo[start : end]
                posInfo = self.posInfo[start : end]
                tagInfo = self.tagInfo[start : end]
                culster = Cluster(ID, cnInfo, enInfo, posInfo, tagInfo)
                results.append(culster)
                start = index + 1
                IDbase += 1
        if len(results) > 1:
            for index in range(len(results)):
                if index == 0:
                    results[index].nextCluster = results[index + 1]
                if index == len(results)-1:
                    results[index].nextCluster = results[index - 1]
                elif 1 <= index <= len(results):
                    results[index].preSent = results[index - 1]
                    results[index].nextSent = results[index + 1]
        return results       
        
        


class Cluster(Sentence):
    ID = ''
    enInfo = []
    cnInfo = []
    tagInfo = []
    posInfo = []
    cnStr = ""
    preCluster = None
    nextCluster = None
    
    def htmlReady(self):
        self.cnStr = ''.join(self.cnInfo)
        
    def __init__(self, ID = 0, cnInfo = None, enInfo = None, posInfo = None, tagInfo = None,):
        self.ID = ID
        self.cnInfo = cnInfo
        self.enInfo = enInfo
        self.tagInfo = tagInfo
        self.posInfo = posInfo
        
    
    def __str__(self):
        if self is None:
            return ''
        sent = "{s}\n"
        sent += "ID: \t" + self.ID.decode() + "\n"
        sent += "{s}"
        return sent.format(s = "-"*20)
    


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
    
    def saveCorpus(self):
        import os
        import pickle
        path = os.path.abspath(__file__)
        path = os.getcwd()[:-5]
        output = path + "data/"
        with open( output + self.name + ".db") as f:
            pickle.dump(self, f)
        print("Corpus: " + self.name +" was stored.")

    def __init__(self, name=None):
        if name is None:
            name = u"Default Unnamed Corpus"
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
    posPattern = None
    result = None
    
    def __init__(self, taskName, taskDesc, cnPattern = None,
                 posPattern = None):
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
        self.posPattern = posPattern
    
    def __str__(self):
        result = "{s}"
        result += self.name.decode() + "\n"
        result += self.desc.decode() + "\n"
        result += "{s}"
        return result.format(s = "+"*40+"\n")
        







