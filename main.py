# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:47:10 2013

@author: yuankunluo
"""
import controller
import search
import output
import pickle

fs = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R']

def start(cnXML, enXML):
    ct = controller.Controller()
    c = ct.addXMLToCorpus(cnXML,enXML)
    return c

def automatMakeCorpus():
    for f in fs:
        try:
            start("lcmc/cn/LCMC_"+f+".xml", "lcmc/en/LCMC_"+f+".xml")
        except:
            print("Make Corpus for %s failure!"%(f))

    
def automatHTML(word = '们'):
    """
    """
    import os
    filelist = os.listdir("data/")
    for fname in filelist:
        with open("data/"+ fname, "rb") as f:
            c = pickle.load(f)
            result1 = search.searchCNWordandHighlight(c, word)
            result2 = search.searchWordWithPos(c,word)
            output.outputHtml(c,result1, "men")
            output.outputHtml(c,result2,"menwithn")
    
    