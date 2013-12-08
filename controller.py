# -*- coding: utf-8 -*-
from model import Sentence
from model import Cluster
from model import Corpus
from model import Task
import copy
import re
from xml.etree.ElementTree import parse
import time



def sortDict(inputDict):
    """Sort the inputDict.
    
    :param inputDict: the Dict to sort
    :type inputDict: dict
    :param rank: A number to indicate how many items will be ranked
    :type rank: Int
    :return: OrderedDict
    """
    # first sort this input dict
    from collections import OrderedDict
    ranking = OrderedDict(sorted(inputDict.items(), key=lambda t: t[0]))
    return ranking

class Controller:
    """
	Controller to all things
    """

    def parseXML(self, xml):
        """Parse a XML data.
        
        :param self: A controller instance
        :type self: A controller instance
        :param xml: A xml data name
        :type xml: String
        :returns: a Dict 
        """
        results = {}
        results['contents'] = {}
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
                    # sentence level
                    for sentence in sentences:
                        sentNr = sentence.attrib['n'].strip()  # sentence Nr.
                        sentNr =  sectionID+"-"+fileID+"-"+sentNr                        
                        cps = sentence.getchildren()  # compenents in every sentence
                        textInfo = []
                        tagInfo = []
                        posInfo = []                        
                        # compenent level                        
                        for cp in cps:
                            tag = unicode(cp.tag)  # tag
                            if tag == u'gap':
                                continue
                            try:
                                pos = unicode(cp.attrib['POS'])  # pos-attr
                            except:
                                print("Sent " + sentNr +" has no pos attrib")
                                continue
                            text = unicode(cp.text)  # text
                            textInfo.append(text)
                            tagInfo.append(tag)
                            posInfo.append(pos)
                        # add sent into result['contens']
                        results['contents'][sentNr] = (textInfo, tagInfo, posInfo)
                #print("Sent Nr. %s was parsed!"%(sentNr))
        results['contents'] = sortDict(results['contents'])
        results['volume'] = len(results['contents'])
        return results
        

    def mixCnEn(self, cnResults, enResults):
        """Mix enResult into cnResult
        
        """
        result = {}
        if cnResults['volume'] != enResults['volume']:
            print("Mix cnxml and enxml failure!")
            return None
        else:
            result['volume'] = cnResults['volume']
            result['sectionType'] = cnResults['sectionType']
            result['sectionID'] = cnResults['sectionID']
            result['sents'] = {}
            for sentNr in cnResults['contents'].keys():
                content = cnResults['contents'][sentNr]
                cnInfo = content[0]
                tagInfo = content[1]
                posInfo = content[2]
                try:
                    enInfo = enResults['contents'][sentNr][0]
                except:
                    print("enInfo for sentNr. %s was not found!"%(sentNr))
                    continue
                result['sents'][sentNr] = (cnInfo, enInfo, posInfo, tagInfo)
        result['sents'] = sortDict(result['sents'])
        return result

    def addXMLToCorpus(self, cn_xml, en_xml):
        """Add a cn_xml and en_xml to a corpus
        
        """
        cnResult = self.parseXML(cn_xml)
        enResult = self.parseXML(en_xml)
        mixResult = self.mixCnEn(cnResult, enResult)
        corpus = Corpus("Corpus_"+mixResult['sectionID']+ "_" + mixResult['sectionType'].replace(" ","_") +"_"+ str(mixResult['volume']))
        corpus.sections = mixResult['sectionID']
        for i in range(0,len(mixResult['sents'].keys())):
            sentNr = mixResult['sents'].keys()[i]
            sent = mixResult['sents'][sentNr]            
            cnInfo = sent[0]
            enInfo = sent[1]
            posInfo = sent[2]
            tagInfo = sent[3]
            s = Sentence(sentNr, cnInfo, enInfo, posInfo, tagInfo)
            corpus.sents[i] = s                
        corpus.sents = sortDict(corpus.sents)
        corpus.volume = len(corpus.sents.keys())
        corpus.saveCorpus()
        return corpus
            
        

        


                    


        
        
        




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







