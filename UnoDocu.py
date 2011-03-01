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

# FYI: Python-UNO bridge http://udk.openoffice.org/python/python-bridge.html
# This program based on the sorce from http://lucasmanual.com/mywiki/OpenOffice

import uno
import unohelper
import string

#You should have openoffice listening on specified port already. 
#    $ soffice "-accept=socket,host=localhost,port=2002;urp;"

class UnoDocu:
    def __init__(self, port=2002):
        '''Load necessary items'''
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext(\
                "com.sun.star.bridge.UnoUrlResolver", local)
        self._ctx = resolver.resolve(\
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        self._desktop = self._ctx.ServiceManager.createInstanceWithContext(\
                "com.sun.star.frame.Desktop", self._ctx)

    def _path2Url(self, path):
        if not path.startswith('file://'):
            path = os.path.realpath(path)
            if os.path.exists(path):
                return unohelper.systemPathToFileUrl(path)
        print 'ERR! given path is invalid'
        return path

    def loadTemplate(self, path):
        '''Load file template'''
        url = self._path2Url(path)
        self._document = self._desktop.loadComponentFromURL(url ,"_blank", 0, ())
        _cursor = self._document.Text.createTextCursor()

    def findAndReplace(self, find, replace, caseSensitive=False, wordSearch=False):
        #Create Search Descriptor
        search = self._document.createSearchDescriptor()
        search.SearchString = unicode(find)
        search.SearchCaseSensitive = caseSensitive
        search.SearchWords = wordSearch
        print 'starting a search'
        found = self._document.findFirst(search)
        if found:
            print 'Found %s' % find
        while found:
            found.String = string.replace(found.String, unicode(find), unicode(replace))
            found = self._document.findNext(found.End, search)

    def exportToPdf(self, uri):
        '''TODO: http://wiki.services.openoffice.org/wiki/API/Tutorials/PDF_export'''
        pass

    def save(self, path):
        '''Save document'''
        url = self._path2Url(path)
        self._document.storeAsURL(url, ())

    def close(self):
        '''Close'''
        self._document.dispose()

    def sync(self):
        self._ctx.ServiceManager

if __name__ == '__main__':
    import os
    unoDoc = UnoDocu()
    unoDoc.loadTemplate('envelope_templete.odt')

    data = {}
    data['$ADDR_LINE1'] = 'Addr line 1'
    data['$ADDR_LINE2'] = 'Addr line 2'
    data['$NAME'] = 'Gildong Hong'
    data['$PHONE'] = '010-1234-5678'
    data['$CNT'] = '100'
    data['$POST'] = '1 2 3 - 4 5 6'

    for find, replace in data.items():
        unoDoc.findAndReplace(find, replace)

    unoDoc.sync()
#    unoDoc.save('')
#    unoDoc.close()
