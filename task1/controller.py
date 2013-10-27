# -*- coding: utf-8 -*-
from model import Sentence
from model import Cluster
from model import Corpus
from model import Task
import copy
import re
from xml.etree.ElementTree import parse
import time
import os

# - PATH Setting
path = os.path.abspath(__file__)
path = os.getcwd()[:-5]
INPUTPATH = path + 'input/'
OUTPUTPATH = path + 'output/'
os.chdir(path)

class Controller:
    """
	Controller to all things
    """

    datenbank = {}

    def parseXML(self, xml):
        results = {}
        results['contents'] = []
        tree = parse(xml)
        texts = tree.findall('text')
        for text in texts:
            sectionID = text.attrib['ID'].strip()  # sectionID
            results['sectionID'] = sectionID
            sectionType = text.attrib['TYPE']  # textType
            results['sectionType'] = sectionType
            files = text.findall('file')
            for f in files:
                fileID = f.attrib['ID'].strip()  # fileID
                paragraphs = f.findall('p')
                for paragraph in paragraphs:
                    sentences = paragraph.findall('s')
                    for sentence in sentences:
                        sentNr = sentence.attrib['n'].strip()  # sentence Nr.
                        cps = sentence.getchildren()  # compenents in every sentence
                        s = Sentence()  # make a new instance of sentence
                        s.textInfo = []
                        s.linInfo = []
                        s.posInfo = []
                        s.tagInfo = []
                        for cp in cps:
                            tag = unicode(cp.tag)  # tag
                            pos = unicode(cp.attrib['POS'])  # pos-attr
                            text = unicode(cp.text)  # text
                            s.textInfo.append(text)
                            s.tagInfo.append(tag)
                            s.posInfo.append(pos)
                        # append this sent with unique information in corpus
                        # make unique information
                        us = [fileID, sentNr]
                        s.ID = '-'.join(us)
                        results['contents'].append(s)
        results['volume'] = len(results['contents'])
        return results

    def mixCnEn(self, cnResults, enResults):
        results = []  # copy one
        cnList = cnResults['contents']
        enList = enResults['contents']
        if len(cnList) == len(enList):
            for i in range(0, len(cnList)):
                cnSent = cnList[i]
                enSent = enList[i]
                if cnSent.ID != enSent.ID:
                    raise Exception()
                else:
                    cnSent.cnInfo = cnSent.textInfo[:]
                    cnSent.enInfo = enSent.textInfo[:]
                    results.append(cnSent)
                    # print(cnSent)
            # print(len(results))
            return results
        else:
            raise Exception()
            print("mix failure.")


    def addXMLToCorpus(self, corpus, cn_xml, en_xml):
        if isinstance(corpus, Corpus):
            cnResults = self.parseXML(cn_xml)
            enResults = self.parseXML(en_xml)
            keys = ['sectionID', 'sectionType', 'volume']
            # get the volume from these two input xml
            cInfo = "-".join([str(cnResults[value]) for value in keys])
            eInfo = "-".join([str(enResults[value]) for value in keys])
            # get sections of this corpus
            sections = corpus.sections
            contentsList = corpus.contentsList # List in Corpus
            contentsDict = corpus.contentsDict # Dict in Corpus
            if cInfo == eInfo:  # test if two xml parsed data is same
                results = self.mixCnEn(cnResults, enResults)
                sections.append((cnResults['sectionID'],
                cnResults['sectionType']))
                for index in range(len(results)):
                    if index == 0:
                        sent = results[0]
                        sent.nextSent = results[1]
                    if index == len(results)-1:
                        sent = results[index]
                        sent.preSent = results[index - 1]
                    elif 1 <= index <= len(results):
                        sent = results[index]
                        sent.preSent = results[index - 1]
                        sent.nextSent = results[index + 1]
                    sent.clusters = sent.makeClusters()
                    contentsList.append(sent)
                    contentsDict[sent.ID] = sent
                return True
        else:
            print("Corpus was not fund.")
            return False

    def makeCorpus(self, name="Default Corpus"):
        corpus = Corpus(name)
        self.datenbank[name] = corpus
        return corpus

    def getCorpus(self, name):
        return self.datenbank[name]

    def __repr__(self):
        return "I am a Controller"

    def mixSearch(self, taskName = "", cnPattern = None, enPattern = None ):
        pass

    def clusterSearch(self, corpus, task, output = None):
        results = {'task': task}
        results['sentences'] = []
        cnPattern = task.cnPattern
        posPattern = task.posPattern
        for s in corpus.contentsList:
            sent = copy.copy(s)
            for c in sent.clusters:
                cluster = copy.copy(c)
                cluster.htmlReady() # make Ready for Html
                posInfo = ''.join(cluster.posInfo)
                cnInfo = ''.join(cluster.cnInfo)
                # case 1:  both pattern exist
                if cnPattern and posPattern:
                    print("Both Pattern search!")
                # case 2: only cnPattern exist
                elif cnPattern:
                    print("Only cnPattern search!")
                # case 3: only enPattern exist
                elif posPattern:
                    matches = re.finditer(posPattern, posInfo)
                if matches:
                    cnStr = cluster.cnStr
                    for m in matches:
                        emStart = m.start()
                        emEnd = m.end()
                        cluster.cnStr = '<em>' +cnStr[:emStart+1] + cnStr[emStart + 1 : emEnd] + "</em>" + cnStr[emEnd+1 :]
                    print(cluster)




#===================================================================
# Test Code
#
# 测试代码
#===================================================================
if __name__ == '__main__':

    # --------------
    ct = Controller()
    c = ct.makeCorpus("Test Corpus")
    ct.addXMLToCorpus(c, INPUTPATH + 'lcmc/c1.xml', INPUTPATH + 'lcmc/e1.xml')
    s = c.getSentByID("A01-0009")
    t1 = Task("Aufgabe_1", "列举语料库中所有主语以单独名词形式,（没有加任何修饰成分）出现的句子，plus前面一句和后面一句\
（共三句话）。例：太阳晒屁股了", None, r'^((n|ng|nr|ns|nt|nx|nz))+?v[^v|vn]*$')
    ct.clusterSearch(c, t1)







