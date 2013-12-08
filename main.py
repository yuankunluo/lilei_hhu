# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:47:10 2013

@author: yuankunluo
"""
import controller
import search
import output

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
    fs = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R']
    for f in fs:
        try:
            c = start(f, "LCMC/cn/LCMC_"+f+".xml", "LCMC/en/LCMC_"+f+".xml")
            s = search.searchCNWordandHighlight(c,word)
            output.outputHtml(s,"output/html/"+ f,f)
        except:
            continue
    