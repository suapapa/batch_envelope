#!/usr/bin/python
# -*- coding: utf-8 -*-

# UnoDocu.py - easy frontend for Python-UNO,
#     http://udk.openoffice.org/python/python-bridge.html
#
# Copyright (C) 2011 Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program based on the sorce from http://lucasmanual.com/mywiki/OpenOffice

import uno
import string

#You should have openoffice listening on specified port already. 
#    $ soffice "-accept=socket,host=localhost,port=2002;urp;"

class UnoDocu:
    def __init__(self, port=2002):
        '''Load necessary items'''
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        self._desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)

    def loadTemplate(self, uri):
        '''Load file template'''
        #_document = _desktop.loadComponentFromURL("file:///home/lucas/TemplateLetter.odt" ,"_blank", 0, ())
        self._document = self._desktop.loadComponentFromURL(uri ,"_blank", 0, ())
        _cursor = self._document.Text.createTextCursor()

    def findAndReplace(self, find=None, replace=None):
        #Create Search Descriptor
        search = self._document.createSearchDescriptor()
        #What to search for
        search.SearchString = unicode(find)
        #search.SearchCaseSensitive = True
        #search.SearchWords = True
        print 'starting a search'
        found = self._document.findFirst(search)
        if found:
            print 'Found %s' % find
        while found:
            found.String = string.replace(found.String, unicode(find), unicode(replace))
            found = self._document.findNext(found.End, search)

    def save(self, uri):
        '''Save document'''
        #document.storeAsURL("file:///home/lucas/letter2.odt",())
        self._document.storeAsURL(uri, ())

    def close(self):
        '''Close'''
        self._document.dispose()

if __name__ == '__main__':
    import os
    unoDoc = UnoDocu()
    unoDoc.loadTemplate('file://' + os.path.realpath('envelope_templete.odt'))

    data = {}
    data['$ADDR_LINE1'] = 'Addr line 1'
    data['$ADDR_LINE2'] = 'Addr line 2'
    data['$NAME'] = 'Gildong Hong'
    data['$PHONE'] = '010-1234-5678'
    data['$CNT'] = '100'
    data['$POST'] = '1 2 3 - 4 5 6'

    for find, replace in data.items():
        unoDoc.findAndReplace(find, replace)

#    unoDoc.save('')
    unoDoc.close()
