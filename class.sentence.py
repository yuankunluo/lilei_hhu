# -*- coding: utf-8 -*-
"""
@author yuankun luo
@copyright yuankun.luo@hhu.de
"""
# use xml parse
from xml.etree.ElementTree import parse

import os
os.chdir('/home/yuankunluo/workspace/lilei_programm')
import re
"""
The globle linguistcs information caterogie
"""
ADJ = ['a','ad','ag','an','b','bg']
CON = ['c','cg']
ADV = ['d','dg']
VERB = ['v','vd','vg','vn',]
NOUN = ['n','ng','nr','ns','nt','nx','nz']
#===================================================================
# Some constants we use as globe 
#===================================================================
U8 = 'utf-8'
AUF_1 = '\n\t任务1：\n\t列举语料库中所有主语以单独名词形式\
（没有加任何修饰成分）出现的句子，plus前面一句和后面一句\
（共三句话）。\n\t例：太阳晒屁股了。\n'
AUF_2 = '\n\t任务2\n\t列举语料库中所有宾语以单独名词形式\
（没有加任何修饰成分）出现的句子，\
plus前面一句和后面一句（共三句话）。\
\n\t例：我买了书。'
AUF_3_1 = '\n\t任务3：\n\t列举语料库中所有主语加\“这/那\”出现的句子\
（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。\
\n\t例：这/那本书很贵。\n\t带量词'
AUF_3_2 = '\n\t任务3：\n\t列举语料库中所有主语加\“这/那\”出现的句子\
（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。\
\n\t例：这/那本书很贵。\n\t不带量词'
AUF_4 = '\n\t任务4\n\t列举语料库中所有宾语加\“这/那\”出现的句子\
（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。\
\n\t例：我买了这/那本书。'
AUF_5_1 = '\n\t任务5_1：\n\t列举语料库中所有主语以两个名词或两个名词以上的形式\
（允许加修饰成分，如“把XX” “给XX”  “这/那+名词” \
（分成带量词和不带量词两类）- “我把书买了。”，“我给那（栋）房子付了头期款。”）\
出现的句子，plus前面一句和后面一句（共三句话）。\
\n\t例：孩子把饭吃了。孩子给我一颗糖。孩子把那（副）药吃了。\n\t带量词\n\n\n\t{这个例子是不是不对?\
例子说所的是宾语，而任务是说主语，所以我找的是以两个或者两个以上名词作为主语的句子。}'
AUF_5_2 = '\n\t任务5：\n\t列举语料库中所有主语以两个名词或两个名词以上的形式\
（允许加修饰成分，如\“把XX\”\“给XX\”\“这/那+名词\” \
（分成带量词和不带量词两类）- \“我把书买了。\”，\“我给那（栋）房子付了头期款。\”）\
出现的句子，plus前面一句和后面一句（共三句话）。\
\n\t例：孩子把饭吃了。孩子给我一颗糖。孩子把那（副）药吃了。\n\t不带量词\n\n\n\t{这个例子是不是不对?\
例子说所的是宾语，而任务是说主语，所以我找的是以两个或者两个以上名词作为主语的句子。}'
AUF_6_1 = '\n\t任务6_1\n\t列举语料库中所有宾语以两个名词或两个名词以上的形式\
（除名词外没有加任何修饰成分）出现的句子，plus前面一句和后面一句（共三句话）。'
AUF_6_2_a = '\n\t任务6_2\n\t列举语料库中所有宾语以两个名词或两个名词以上的形式\
（允许修饰成分，直接宾语，间接宾语，“这/那+名词”（分成带量词和不带量词两类））出现的句子，\
plus前面一句和后面一句（共三句话）。\n\t例：孩子把狗食给猫吃了。孩子把这（盒）狗食给那（支）猫吃了。\n\t带量词'
AUF_6_2_b = '\n\t任务6_2\n\t列举语料库中所有宾语以两个名词或两个名词以上的形式\
（允许修饰成分，直接宾语，间接宾语，“这/那+名词”（分成带量词和不带量词两类））出现的句子，\
plus前面一句和后面一句（共三句话）。\n\t例：孩子把狗食给猫吃了。孩子把这（盒）狗食给那（支）猫吃了。\n\t不带量词'
AUF_7 = '\n\t任务7\n\t列举“动词+了”的结构的句子。plus前面一句和后面一句（共三句话）。\n\t例：孩子吃了饭。'
AUF_8 = '\n\t任务8\n\t列举一句中出现了两个或两个以上“了”的句子。plus前面一句和后面一句（共三句话）。\n\t例：孩子吃了饭了。'
AUF_9 = '\n\t任务9\n\t列举即出现“动词+了”结构，又出现“了”在句尾的句子。\
plus前面一句和后面一句（共三句话）。\n\t例：孩子吃了饭了。'
AUF_10 = '\n\t任务10\n\t列举“我，你，他/她/它，您，咱，俺，我们，你们，\
他们/她们/它们，您们，咱们，俺们+ 的 + 名词”结构的句子。\
plus前面一句和后面一句（共三句话）。\n\t例：我的母亲是老师。'
AUF_11 = '\n\t任务11\n\t列举“我，你，他/她/它，您，咱，俺，我们，你们，\
他们/她们/它们，您们，咱们，俺们直接 + 名词”结构的句子。\n\
plus前面一句和后面一句（共三句话）。\
\n\t例：我老师很喜欢骂人。'
AUF_12_A = '\n\t任务11\n\t列举“一 + 量词 + 名词” 结构的句子。\
plus前面一句和后面一句（共三句话）。\n\t例：一位女士走上了讲台。'
AUF_12_B = '\n\t任务12_b\
\n\t列举“一 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。\
\n\t例：一小孩掉进了水里。'
AUF_13_A = '\n\t任务13_a\
\n\t列举“有+ 一 + 量词 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。\
\n\t例：树上有一支小鸟。树上有一些花开了。'
AUF_13_B = '\n\t任务13_b\n\t列举“有+ 量词 + 名词” 结构的句子。\
\n\tplus前面一句和后面一句（共三句话）。\
\n\t例：树上有支小鸟。有些人就是不懂事儿。'
AUF_13_C = '\n\t任务13_c\
\n\t列举“有 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。\
\n\t例：有人来过。树上有花开了'
AUF_14 = '\n\t任务14\
\n\t分开列举“一+ 些+ 名词”，“些+ 名词”和“这/那+ 些+ 名词”的句子。plus前面一句和后面一句（共三句话）。\
\n\t例：树上掉了一些叶子。我出去买些书。这些书都很贵。'
#===================================================================
#class Sentence
#
#Every sentence in this corpus is an instance of this class
#===================================================================
class Sentence:
    """
    This is a sentence class (model)
    @var int sentenceId The identical number of a sentence
    @var list cnInfo The chinese information as a list of words
    @var list pinInfo The pinyin information as a list of pinyin
    @var list linInfo The linguistic information as a pair(catalog, pos)
    """
    #textID=0
    #textType=''
    #fileID = 0
    #sentNr = 0
    unique=''
    cnInfo = []
    cn=''
    pinInfo = []
    pin=''
    linInfo = []
    tagInfo = []
    tag=''
    posInfo = []
    pos=''
    preS = None
    nextS = None


 
    
    def __str__(self):
        cn = ' '.join(self.cnInfo)
        py = '  '.join(self.pinInfo)
        #la = ' '.join([tag for (tag, pos) in self.linInfo])
        lb = ' '.join([pos for (tag, pos) in self.linInfo])
        return "\n{unique}\n\t{lin}{cn}\n\t{lin}{py}\n\t{lin}{lb}".format(
            unique= self.unique, cn=cn, py=py, lb=lb, lin='-'*3+'\n\t')

    def __call__(self):
        self.mixSearch()

    def __repr__(self):
        li = ['unique','cnInfo','pinInfo','tagInfo','posInfo']
        s = '\n'
        for key in li:
           val = str(self.__dict__[key])
           s += key+' : '+val+'\n'
        return s

    def posSearch(self, reg=None):
        sPos = '-'.join(self.posInfo)
        target = re.compile(reg)
        if target.search(sPos):
            return True
        else:
            return False
    def posSearch2(self, reg=None):
        sPos = ''.join(self.posInfo)
        target = re.compile(reg)
        if target.search(sPos):
            return True
        else:
            return False
        
    def inPosSearch(self, reg=None):
        sPos = ''.join(self.posInfo)
        pos = re.sub('w|ew','-',sPos)
        pos = re.sub('-+','-',pos)
        posList = pos.split('-')
        #print(posList)
        pat = re.compile(reg)
        res = []
        for pos in posList:
            if pat.search(pos):
                res.append(1)
            else:
                res.append(0)
        if 1 in res:
            return True
        else:
            return False
        
    def inCnSearch(self, reg=None):
        sCn = ''.join(self.cnInfo)
        cn = re.sub('[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]','-',sCn)
        #print(cn)
        cn = re.sub('-+','-',cn)
        #print(cn)
        cnList = cn.split('-')
        #print(cnList)
        pat = re.compile(reg)
        res = []
        for cn in cnList:
            if pat.search(cn):
                #print(cn)
                res.append(1)
            else:
                res.append(0)
        #print(res)
        if 1 in res:
            return True
        else:
            return False

    def mixSearch(self, cnReg = None, posReg = None, placeholder = None):
        posInfo = self.posInfo.copy()
        cnInfo = self.cnInfo.copy()
        linInfo = [tag for tag, lin in self.linInfo].copy()
        pinInfo = self.pinInfo.copy()
        index = []
        if placeholder is None:
            placeholder = '\u8888'
        for n in range(len(linInfo)):
            if linInfo[n] is 'c':
                index.append(n)
        for n in index:
            posInfo[n] = placeholder
            cnInfo[n] = placeholder
            linInfo[n] = placeholder
            pinInfo[n] = placeholder
        #print(posInfo,'\n', cnInfo,'\n', linInfo)
        self.pposInfo = posList = self.makePart(posInfo)
        self.pcnInfo = cnList = self.makePart(cnInfo)
        self.plinInfo = linList = self.makePart(linInfo)
        self.ppinInfo = pinInfo = self.makePart(pinInfo)
        #print(posList, cnList, linList)
        if (cnReg is not None) and (posReg is not None): 
            cnTarget = re.compile(cnReg)
            posTarget = re.compile(posReg)
            res = []
            for n in range(len(cnList)):
                if cnTarget.search(cnList[n]):
                    if posTarget.search(posList[n]):
                        res.append(1)
                        #print(cnList[n], posList[n])
                else:
                    res.append(0)
            #print(res)
            if 1 in res:
                return True
            else:
                return False
        

    def advMixSearch(self, cnReg = None, posReg = None, placeholder = None):
        posInfo = self.posInfo.copy()
        cnInfo = self.cnInfo.copy()
        linInfo = [tag for tag, lin in self.linInfo].copy()
        index = []
        if placeholder is None:
            placeholder = '\u8888'
        for n in range(len(linInfo)):
            if linInfo[n] is 'c':
                index.append(n)
        for n in index:
            posInfo[n] = placeholder
            cnInfo[n] = placeholder
            linInfo[n] = placeholder
        #print(posInfo,'\n', cnInfo,'\n', linInfo)
        posList = self.makePart(posInfo)
        cnList = self.makePart(cnInfo)
        linList = self.makePart(linInfo)
        #print(posList, cnList, linList)
        cnTarget = re.compile(cnReg)
        posTarget = re.compile(posReg)
        res = []
        for n in range(len(cnList)):
            if cnTarget.search(cnList[n]):
                if posTarget.search(posList[n]):
                    res.append(1)
                    #print(cnList[n], posList[n])
            else:
                res.append(0)
        #print(res)
        if 1 in res:
            return True
        else:
            return False
        
        
            

    def cnSearch(self, reg=None):
        sCN = ''.join(self.cnInfo)
        target = re.compile(reg)
        if target.search(sCN):
            return True
        else:
            return False
        
    def makePart(self, li=None, placeholder=None):
        if placeholder is None:
            placeholder = '\u8888'
        string = ''.join(li)
        cleanS = re.sub('(\u8888)+','_',string)
        li = cleanS.split('_')
        return li
        
        
        
            
    
    
#===================================================================
#Class Text
#
#For now i dont use this class
#===================================================================
class Text:
    """
    @var content
    @var int fileId The identical number of this file in this corpus
    @var int textId The identical number of the text in this corpus
    @var string textType The type of thie text
    """
    fileId = 0
    textID=0
    textType=''
    content=[]


#===================================================================
#Class Controller
#
#To oprate the corpus
#===================================================================
class Controller:
    """
    Controller is a class.
    @var dict corpus The corpus is a dict to storge all sentences
    """

    corpusD = {}
    corpusL=[]

    def parseXML(self, cxml, exml):
        self.parseCXML(cxml)
        self.parseEXML(exml)


    def addToCorpus(self, id, text):
        if isinstance(id,int) and isinstance(text,Text):
            self.corpus[id] = text
            print('addToCorpus: True')
            return True
        else:
            print('addToCorpus: False')
            return False


    """
    Parse first the chineses data
    """
    def parseCXML(self,cxmldata):
        tree = parse(cxmldata)
        texts = tree.findall('text')
        for text in texts:
            textID = text.attrib['ID'].strip() # textID
            textType = text.attrib['TYPE'] #textType
            files = text.findall('file')
            for file in files:
                fileID = file.attrib['ID'].strip() #fileID
                paragraphs = file.findall('p')
                for paragraph in paragraphs:
                    sentences = paragraph.findall('s')
                    for sentence in sentences:
                        sentNr = sentence.attrib['n'].strip() # sentence Nr.
                        cps = sentence.getchildren()
                        s = Sentence() # make a new instance of sentence
                        #s.textID = textID
                        #s.textType = textType
                        #s.fileID = fileID
                        #s.sentNr = sentNr
                        s.cnInfo = []
                        s.linInfo =[]
                        for cp in cps:
                            tag = cp.tag
                            pos = cp.attrib['POS']
                            text = cp.text
                            lin = (tag, pos)
                            s.cnInfo.append(text)
                            s.linInfo.append(lin)
                        # append this sent with unique information in corpus
                        # make unique information
                        us = [textID, fileID, sentNr]
                        s.unique = '-'.join(us)
                        s.tagInfo = [tag for (tag, pos) in s.linInfo]
                        s.posInfo = [pos for (tag, pos) in s.linInfo]
                        self.corpusD[s.unique] = s
                        self.corpusL.append(s)
                        
                        

    """
    This methode parse  the english xml data,
    then check if this english
    """            
    def parseEXML(self, exmldata):

        tree = parse(exmldata)
        texts = tree.findall('text')
        for text in texts:
            textID = text.attrib['ID'].strip() # textID
            textType = text.attrib['TYPE'] #textType
            files = text.findall('file')
            for file in files:
                fileID = file.attrib['ID'].strip() #fileID
                paragraphs = file.findall('p')
                for paragraph in paragraphs:
                    sentences = paragraph.findall('s')
                    for sentence in sentences:
                        sentNr = sentence.attrib['n'].strip() # sentence Nr.
                        cps = sentence.getchildren()
                        linInfo =[]
                        pinInfo =[]
                        for cp in cps:
                            tag = cp.tag
                            pos = cp.attrib['POS']
                            lin = (tag, pos)
                            text = cp.text
                            pinInfo.append(text)
                            linInfo.append(lin)
                        us = [textID, fileID, sentNr]
                        eunique = '-'.join(us)
                        s = self.corpusD[eunique]
                        s.pinInfo = pinInfo
                        #self.corpusD.pop(s.unique) # pop sentence out of the corpusD


    """
    posSearch
    @para   List  corpus
    @para   Reg reg
    """
    def posSearch(self, corpus=None, reg=None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if reg is None:
            reg = '^(n-|ng-|nr-|ns-|nt-|nz-)v-' # default for aufgabe 1
        for index in range(0, len(corpus)):
            if corpus[index].posSearch(reg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results

    """
    posSearch
    @para   List  corpus
    @para   Reg reg
    """
    def posSearch2(self, corpus=None, reg=None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if reg is None:
            reg = '^(n|ng|nr|ns|nt|nz)v' # default for aufgabe 1
        for index in range(0, len(corpus)):
            if corpus[index].posSearch2(reg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results


    def inPosSearch(self, corpus=None, reg=None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if reg is None:
            reg = '^(n|ng|nr|ns|nt|nz)v' # default for aufgabe 1
        for index in range(0, len(corpus)):
            if corpus[index].inPosSearch(reg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results

    
    """
    posSearch
    @para   List  corpus
    @para   Reg reg
    """
    def cnSearch(self, corpus=None, reg=None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if reg is None:
            reg = '^.*(这|那).*$' # default for aufgabe 1
        for index in range(0, len(corpus)):
            if corpus[index].cnSearch(reg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results

    def inCnSearch(self, corpus=None, reg=None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if reg is None:
            reg = '^.*(这|那).*$' # default for aufgabe 1
        for index in range(0, len(corpus)):
            if corpus[index].inCnSearch(reg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results
    
    def mixSearch(self, corpus=None, cnReg=None, posReg = None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if cnReg is None:
            cnReg = '你好' # default for aufgabe 1
        if posReg is None:
            posReg = 'vnn'
        for index in range(0, len(corpus)):
            if corpus[index].mixSearch(cnReg, posReg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results

    def advMixSearch(self, corpus=None, cnReg=None, posReg = None):
        results = {}
        i = 0
        if corpus is None:
            corpus = self.corpusL
        if cnReg is None:
            cnReg = '你好' # default for aufgabe 1
        if posReg is None:
            posReg = 'vnn'
        for index in range(0, len(corpus)):
            if corpus[index].advMixSearch(cnReg, posReg):
                sent = corpus[index]
                if index > 0:
                    preSent = corpus[index-1]
                else:
                    preSent = None
                if index < len(corpus)-1:
                    nextSent = corpus[index+1]
                else:
                    nextSent = None
                r=[]
                for e in [preSent, sent, nextSent]:
                    if e is not None:
                        r.append(e)
                results[i] = r
                i = i+1
        return results
    

    """
    output methode
    @para   dict    results after search
    @para   str fileName
    """
    def output (self, auf = None, corpus = None, results = None, file = None):
        with open(file, 'wb') as file:
            file.write(str('='*80 +'\n' + auf + '\n\n' + '='*80 + '\n' ).encode(U8))
            file.write(str('\n语料库: ' + str(corpus[0].unique[0:1]) +' 共有 '+ str(len(corpus)) +' 句句子。').encode(U8))
            ration = len(results)/ len(corpus)
            ra = "{0:.0f}%".format(ration * 100)
            file.write(str('\n在此语料库文件中共找出: '+ str(len(results)) + '组句子符合要求。\n比例约为： '+str(ra)+'\n'+ '-'*80+'\n\n').encode(U8))
            i = 1
            for key in results.keys():
                file.write(str('\n\n结果： '+ str(i)).encode(U8))
                sents = results[key]
                file.write(str('\n'+'-'*30+'\n').encode(U8))
                for sent in sents:
                    file.write(str(str(sent) + '\n').encode(U8))
                file.write(str('\n'+'-'*30+'\n').encode(U8))
                i = i+1
            
            
                        
    """
    -------------------------------------------------------------------
    任务1：
    列举语料库中所有主语以单独名词形式（没有加任何修饰成分）出现的句子，plus前面一句和后面一句（共三句话）。
    例：太阳晒屁股了。
    -------------------------------------------------------------------
    return and write the processed results into a .txt data.
    @para   list    corpus
    @reg    str reg
    """
    def aufgabe1(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        if reg is None:
            reg = '^(n-|ng-|nr-|ns-|nt-|nz-|r-|rg-)(v|vg|vd).*$'
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_1.txt'
        results = self.posSearch(corpus, reg)
        self.output(AUF_1,corpus,results,file)

    """
    任务2：
    列举语料库中所有宾语以单独名词形式（没有加任何修饰成分）出现的句子，plus前面一句和后面一句（共三句话）。
    例：我买了书。
    """
    def aufgabe2(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        if reg is None:
            reg = '^.*((v)-(n-|ng-|nr-|ns-|nt-|nz-|r-|rg-)){1,1}ew$'
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_2.txt'
        results = self.posSearch(corpus, reg)
        self.output(AUF_2,corpus,results,file)

    """
    任务3：
    列举语料库中所有主语加“这/那”出现的句子（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。
    例：这/那本书很贵。
    带量词
    """
    def aufgabe3_1(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_3_1.txt'
        if reg is None:
            cnReg = '.*(那|这).*'
            posReg = '^r-(q|qg).*$|w-r-(q|qq).*'
            #posReg = '(w-)?[^v]-r-(q|qg)(-a|-ad|-ag|-an)*(-n|-nr|-ng|-ns|-nt|-nx|-nz)*(-v|-vd|-vg|-vn).*'
        cnResults = self.cnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].posSearch(posReg):
                posResults.pop(key)
        self.output(AUF_3_1,corpus,posResults,file)
    
    """
    任务3_2：
    列举语料库中所有主语加“这/那”出现的句子（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。
    例：这/那本书很贵。
    不带量词
    """
    def aufgabe3_2(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_3_2.txt'
        if reg is None:
            cnReg = '.*(那|这).*'
            posReg = '^r(-n|-nr|-ng|-ns|-nt|-nx|-nz)+.*$'
            #posReg = '(w-)?[^v]-r-(q|qg)(-a|-ad|-ag|-an)*(-n|-nr|-ng|-ns|-nt|-nx|-nz)*(-v|-vd|-vg|-vn).*'
        cnResults = self.cnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].posSearch(posReg):
                posResults.pop(key)
        self.output(AUF_3_2,corpus,posResults,file)

    """
    任务4:
    列举语料库中所有宾语加“这/那”出现的句子（分成带量词和不带量词两类），plus前面一句和后面一句（共三句话）。
    例：我买了这/那本书。
    """
    def aufgabe4(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_4.txt'
        if reg is None:
            cnReg = '.*(那|这).*'
            posReg = '^.*(v|vn|vd|vg){1,1}-r-(q|qg)?(-n|-nr|-ng|-ns|-nt|-nx|-nz)*'
            #posReg = '(w-)?[^v]-r-(q|qg)(-a|-ad|-ag|-an)*(-n|-nr|-ng|-ns|-nt|-nx|-nz)*(-v|-vd|-vg|-vn).*'
        cnResults = self.cnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].posSearch(posReg):
                posResults.pop(key)
        self.output(AUF_4,corpus,posResults,file)
        

    """
    任务5_1：
    列举语料库中所有主语以两个名词或两个名词以上的形式（允许加修饰成分，如“把XX”“给XX”“这/那+名词” （分成带量词和不带量词两类）
    -
    “我把书买了。”，“我给那（栋）房子付了头期款。”）出现的句子，plus前面一句和后面一句（共三句话）。
    例：孩子把饭吃了。孩子给我一颗糖。孩子把那（副）药吃了。
    带量词
    """
    def aufgabe5_1(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_5_1.txt'
        if reg is None:
            posReg = '(^|w)[^p|pg](a|ad|ag|an|b|bg)*(m|mg)*(q|qg)+(nr|n|ng|ns|nt|nx|nz){2,}v.*(w|ew)'
        posResults = self.posSearch2(corpus, posReg)
        self.output(AUF_5_1,corpus,posResults,file)


    """
    任务5_2：
    列举语料库中所有主语以两个名词或两个名词以上的形式（允许加修饰成分，如“把XX”“给XX”“这/那+名词” （分成带量词和不带量词两类）
    -
    “我把书买了。”，“我给那（栋）房子付了头期款。”）出现的句子，plus前面一句和后面一句（共三句话）。
    例：孩子把饭吃了。孩子给我一颗糖。孩子把那（副）药吃了。
    不带量词
    """
    def aufgabe5_2(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_5_2.txt'
        if reg is None:
            posReg = '(^|w)[^p|pg](a|ad|ag|an|b|bg)*(m|mg)*(nr|n|ng|ns|nt|nx|nz){2,}v.*(w|ew)'
        posResults = self.posSearch2(corpus, posReg)
        self.output(AUF_5_2,corpus,posResults,file)

    """
    任务6_1
    列举语料库中所有宾语以两个名词或两个名词以上的形式（除名词外没有加任何修饰成分）出现的句子，plus前面一句和后面一句（共三句话）。
    。。。。。
    """
    def aufgabe6_1(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_6_1.txt'
        if reg is None:
            posReg = '(^|w).*v-(n-|ng-|nr-|ns-|nt-|nx-|nz-){2,}[^u]*(w|ew)'
        posResults = self.posSearch(corpus, posReg)
        self.output(AUF_6_1,corpus,posResults,file)

    """
    任务6_2_a
    列举语料库中所有宾语以两个名词或两个名词以上的形式（允许修饰成分，直接宾语，间接宾语，“这/那+名词”（分成带量词和不带量词两类））出现的句子，plus前面一句和后面一句（共三句话）。
    例：孩子把狗食给猫吃了。孩子把这（盒）狗食给那（支）猫吃了。
    """
    def aufgabe6_2_a(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_6_2_a.txt'
        if reg is None:
            posReg = '(^|w).*v-(m-|mg-)*(q-|qg-)+(a-|ad-|ag-|an-|b-|bg-|u-)*(n-|ng-|nr-|ns-|nt-|nx-|nz-){2,}[^u]*(w|ew)'
        posResults = self.posSearch(corpus, posReg)
        self.output(AUF_6_2_a,corpus,posResults,file)
            
    """
    任务6_2_b
    列举语料库中所有宾语以两个名词或两个名词以上的形式（允许修饰成分，直接宾语，间接宾语，“这/那+名词”（分成带量词和不带量词两类））出现的句子，plus前面一句和后面一句（共三句话）。
    例：孩子把狗食给猫吃了。孩子把这（盒）狗食给那（支）猫吃了。
    """
    def aufgabe6_2_b(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_6_2_b.txt'
        if reg is None:
            posReg = '(^|w).*v-(m-|mg-)*(a-|ad-|ag-|an-|b-|bg-|u-)*(n-|ng-|nr-|ns-|nt-|nx-|nz-){2,}[^u]*(w|ew)'
        posResults = self.posSearch(corpus, posReg)
        self.output(AUF_6_2_a,corpus,posResults,file)

    """
    任务7
    列举“动词+了”的结构的句子。plus前面一句和后面一句（共三句话）。
    例：孩子吃了饭。
    """
    def aufgabe7(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_7.txt'
        if reg is None:
            cnReg = '了'
            posReg = '(^|)[^v]*(v|vn|vd|vg)u.*(w|ew)'
            #posReg = '(w-)?[^v]-r-(q|qg)(-a|-ad|-ag|-an)*(-n|-nr|-ng|-ns|-nt|-nx|-nz)*(-v|-vd|-vg|-vn).*'
        cnResults = self.cnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].posSearch2(posReg):
                posResults.pop(key)
        self.output(AUF_7,corpus,posResults,file)
        
    """
    任务8
    列举一句中出现了两个或两个以上“了”的句子。plus前面一句和后面一句（共三句话）。
    例：孩子吃了饭了。
    """
    def aufgabe8(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_8.txt'
        if reg is None:
            cnReg = '了.*了'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '.*'
        cnResults = self.inCnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].inPosSearch(posReg):
                posResults.pop(key)
        self.output(AUF_8,corpus,posResults,file)

    """
    任务9
    列举即出现“动词+了”结构，又出现“了”在句尾的句子。plus前面一句和后面一句（共三句话）。
    例：孩子吃了饭了。
    """
    def aufgabe9(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_9.txt'
        if reg is None:
            cnReg = '了.*了$'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '.*'
        cnResults = self.inCnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].inPosSearch(posReg):
                posResults.pop(key)
        self.output(AUF_9,corpus,posResults,file)

    """
    任务10
    列举“我，你，他/她/它，您，咱，俺，我们，你们，他们/她们/它们，您们，咱们，俺们+ 的 + 名词”结构的句子。plus前面一句和后面一句（共三句话）。
    例：我的母亲是老师。
    """
    def aufgabe10(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_10.txt'
        if reg is None:
            cnReg = '(我|你|他|她|它|您|咱|俺|我们|你们|他们|她们|它们|您们|咱们|俺们)的'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(r|rg)u'
        cnResults = self.inCnSearch(corpus, cnReg)
        posResults = cnResults.copy()
        for key in cnResults.keys():
            if not cnResults[key][1].inPosSearch(posReg):
                posResults.pop(key)
        self.output(AUF_10,corpus,posResults,file)

    """
    任务11
    列举“我，你，他/她/它，您，咱，俺，我们，你们，他们/她们/它们，您们，咱们，俺们直接 + 名词”结构的句子。plus前面一句和后面一句（共三句话）。
    例：我老师很喜欢骂人。
    """
    def aufgabe11(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_11.txt'
        if reg is None:
            cnReg = '我|你|他|她|它|您|咱|俺|我们|你们|他们|她们|它们|您们|咱们|俺们'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(r|rg)+(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg,posReg)
        self.output(AUF_11,corpus,cnResults,file)
    """
    任务12_a
    列举“一 + 量词 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。
    例：一位女士走上了讲台。
    """
    def aufgabe12_a(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_12_a.txt'
        if reg is None:
            cnReg = '一'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(m|mg)+(q|qg)+(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg,posReg)
        self.output(AUF_12_A,corpus,cnResults,file)
    """
    任务12_b
    列举“一 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。
    例：一小孩掉进了水里。
    """
    def aufgabe12_b(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_12_b.txt'
        if reg is None:
            cnReg = '一'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(m|mg)+(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_12_B,corpus,cnResults,file)
    """
    任务13_a
    列举“有+ 一 + 量词 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。
    例：树上有一支小鸟。树上有一些花开了。
    --------------
    任务13_b
    列举“有+ 量词 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。
    例：树上有支小鸟。有些人就是不懂事儿。
    --------------
    任务13_c
    列举“有 + 名词” 结构的句子。plus前面一句和后面一句（共三句话）。
    例：有人来过。树上有花开了
    """
    def aufgabe13(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_13_a.txt'
        if reg is None:
            cnReg = '有一'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(m|mg)+(q|qg)+(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_13_A,corpus,cnResults,file)
        
        file = directory + 'Aufgabe_13_b.txt'
        cnReg = '有'
        #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
        posReg = '(m|mg)+(q|qg)+(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_13_B,corpus,cnResults,file)

        file = directory + 'Aufgabe_13_c.txt'
        cnReg = '有'
        #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
        posReg = 'v(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_13_C,corpus,cnResults,file)
    """
    任务14
    分开列举“一+ 些+ 名词”，“些+ 名词”和“这/那+ 些+ 名词”的句子。plus前面一句和后面一句（共三句话）。
    例：树上掉了一些叶子。我出去买些书。这些书都很贵。
    """
    def aufgabe14(self, corpus=None, reg = None, fileName=None):
        if corpus is None:
            corpus = self.corpusL
        corpusName = corpus[0].unique[0:1]
        directory = 'output\\'+ corpusName + '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if fileName is None:
            file = directory + 'Aufgabe_14_a.txt'
        if reg is None:
            cnReg = '一些'
            #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
            posReg = '(m|mg)(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_14,corpus,cnResults,file)
        
        file = directory + 'Aufgabe_14_b.txt'
        cnReg = '这些|那些'
        #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
        posReg = 'r(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_14,corpus,cnResults,file)

        file = directory + 'Aufgabe_14_c.txt'
        cnReg = '[^这那哪有一某]些'
        #posReg = '(^|)(^v|vn|vd|vg)*(v|vn|vd|vg)u[^u|v]*u(w|ew)'
        posReg = 'r(n|ng|nr|ns|nt|nx|nz)+'
        cnResults = self.mixSearch(corpus, cnReg, posReg)
        self.output(AUF_14,corpus,cnResults,file)




#===================================================================
#Test Code
#
#测试代码
#===================================================================


if __name__ == '__main__':

    t = Text()
    c = Controller()
    c.parseXML('c1.xml','e1.xml')
    tt = parse('c1.xml')
    sCorpus = c.corpusL
    s = c.corpusL[200]
    #r = c.aufgabe1()
    r1 = c.aufgabe1(sCorpus)
    r2 = c.aufgabe2(sCorpus)
    r3_1 = c.aufgabe3_1(sCorpus)
    r3_2 = c.aufgabe3_2(sCorpus)
    r4 = c.aufgabe4(sCorpus)
    r5_1 = c.aufgabe5_1(sCorpus)
    r5_2 = c.aufgabe5_2(sCorpus)
    r6_1 = c.aufgabe6_1(sCorpus)
    r6_2_a = c.aufgabe6_2_a(sCorpus)
    r6_2_b = c.aufgabe6_2_b(sCorpus)
    r7 = c.aufgabe7(sCorpus)
    r8 = c.aufgabe8(sCorpus)
    r9 = c.aufgabe9(sCorpus)
    r10 = c.aufgabe10(sCorpus)
    r11 = c.aufgabe11(sCorpus)
    r12_a = c.aufgabe12_a(sCorpus)
    r12_b = c.aufgabe12_b(sCorpus)
    r13_a = c.aufgabe13(sCorpus)
    r14 = c.aufgabe14(sCorpus)
    s1 = sCorpus[0]
