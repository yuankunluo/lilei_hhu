# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:01:42 2013

@author: yuankunluo
"""

import re

def searchCNWordandHighlight(corpus, word):
    """
    搜索们
    """
    word = unicode(word)
    result = []
    mark = []
    for s in corpus.sents.items():
        key = s[0]
        sent = s[1]
        cnInfo = sent.cnInfo
        enInfo = sent.enInfo
        posInfo = sent.posInfo
        for i in range(len(cnInfo)):
            words = cnInfo[i]
            if word in words:
                cnInfo[i] = "<em>" + words + "</em>"
                posInfo[i] = "<em>" + posInfo[i] + "</em>"
                if key not in mark:
                    result.append((cnInfo, enInfo, posInfo))
                    mark.append(key)
    return result

def searchWordWithPos(corpus, word='们', pos='n'):
    """
    搜索出现在名词后面的们
    """
    word = unicode(word)
    result = []
    mark = []
    for s in corpus.sents.items():
        key = s[0]
        sent = s[1]
        cnInfo = sent.cnInfo
        enInfo = sent.enInfo
        posInfo = sent.posInfo
        for i in range(len(cnInfo)):
            words = cnInfo[i]
            if (word in words) and i > 0 :
                lastwords = cnInfo[i-1]
                lastpos = posInfo[i-1]
                if lastpos in ['n','ng','nr','ns','nz','nx','nt']:
                    cnInfo[i] = "<em>" + words + "</em>"
                    posInfo[i] = "<em>" + posInfo[i] + "</em>"
                    cnInfo[i-1] = "<em class =\"norm\">" + lastwords + "</em>"
                    posInfo[i-1] = "<em class =\"norm\">" + lastpos + "</em>"
                    if key not in mark:
                        result.append((cnInfo, enInfo, posInfo))
                        mark.append(key)
    return result
    
        
        
        