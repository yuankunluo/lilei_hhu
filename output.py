# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 16:27:50 2013

@author: yuankunluo
"""

def outputHtml(corpus, tupelList, fname='a'):
    """output html
    """
    head = "<!DOCTYPE html><html><head><title>"+ corpus.name+"</title>"
    style ="<link rel=\"stylesheet\" type=\"text/css\" href=\"css\style.css\">" 
    meta = "<meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width\"></head><body>"
    tail = "</body></html>"
    bodyList = []
    h1 = corpus.html()
    bodyList.append(h1)
    h3 = str(len(tupelList))+ " was gefunden"
    bodyList.append( "<h3>" +  h3 + "</h3>")
    bodyList.append("<ol>")
    for tupe in tupelList:
        cn = ' '.join(tupe[0])
        pos =' '.join(tupe[2])
        cn = "<p>" + cn + "</p>"
        pos = "<p>" + pos + "</p>"
        div = "<li >"+ cn + pos + "</li>"
        bodyList.append(div)
    html = ""
    html += head + style + meta
    for body in bodyList:
        html += body
    html += "</ol>" + tail
    with open("output/html/"+corpus.name[:-4] + "_"+fname+".html",'wb') as f:
        f.write(html)
    print(corpus.name + ".html was stored.")
        
    
        
            
            
    