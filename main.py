# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:47:10 2013

@author: yuankunluo
"""

def start(cnXML, enXML):
    import controller
    import model
    ct = controller.Controller()
    c = ct.makeCorpus("Test Corpus")
    ct.addXMLToCorpus(c, controller.INPUTPATH + cnXML, controller.INPUTPATH + enXML)
    return c