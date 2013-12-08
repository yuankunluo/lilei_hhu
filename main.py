# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:47:10 2013

@author: yuankunluo
"""
import controller
import search
import output

def start(corpusName, cnXML, enXML):
    ct = controller.Controller()
    c = ct.makeCorpus(corpusName.replace(" ","_"))
    ct.addXMLToCorpus(c,cnXML,enXML)
    return c
    
def automatHTML(word = '们'):
    fs = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R']
    for f in fs:
        try:
            c = start(f, "LCMC/cn/LCMC_"+f+".xml", "LCMC/en/LCMC_"+f+".xml")
            s = search.searchCNWordandHighlight(c,word)
            output.outputHtml(s,"output/html/"+ f,f)
        except:
            continue
    