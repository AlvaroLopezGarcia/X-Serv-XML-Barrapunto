#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import feedparser

result=''
title =''
def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            
    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            global result
            global title
            link = ''
            if name == 'title':
                title = self.theContent +"</a>"
                result = title 
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                link = '<a href="' + self.theContent + '">'
                result = link + result
                print (result.encode('utf-8'))
                title = ''
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

theParser.parse("http://barrapunto.com/index.rss")

print ("Parse complete")
