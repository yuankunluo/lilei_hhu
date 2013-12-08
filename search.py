# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:01:42 2013

@author: yuankunluo
"""

import re

def searchCNWordandHighlight(corpus, word):
    word = unicode(word)
    result = []
    sentList = corpus.contentsList
    for sent in sentList:
        cnInfo = sent.cnInfo
        enInfo = sent.enInfo
        posInfo = sent.posInfo
        for i in range(len(cnInfo)):
            words = cnInfo[i]
            if word in words:
                cnInfo[i] = "<em>" + words + "</em>"
                posInfo[i] = "<em>" + posInfo[i] + "</em>"
                result.append((cnInfo, enInfo, posInfo))
    return result
    
        
        
        