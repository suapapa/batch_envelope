#!/usr/bin/python
# -*- coding: utf-8 -*-

# PostKr.py - 인터넷우체국 오픈API 파이썬 프론트엔드 
#
# Copyright (C) 2011 Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# FYI: 인터넷우체국 오픈API 이용방법:
# http://biz.epost.go.kr/eportal/custom/custom_10.jsp?subGubun=sub_4&subGubun_1=cum_20

import urllib2
from BeautifulSoup import BeautifulStoneSoup as BS

class PostKr:
    _url = 'http://biz.epost.go.kr/KpostPortal/openapi?regkey=%s&target=%s&query=%s'
    def __init__(self, regKey=''):
        if not regKey:
            print 'ERR: You should receive your own api-key from following link:'
            print 'http://biz.epost.go.kr/eportal/custom/custom_11.jsp?subGubun=sub_3&subGubun_1=cum_19&gubun=m07'
        else:
            self._regKey = regKey

    def _postRequest(self, target, query):
        query = query.encode('euc-kr')
        url = self._url%(self._regKey, target, urllib2.quote(query))
        # print url
        req = urllib2.Request(url, None, {"Accept-Language":"ko"})
        return urllib2.urlopen(req).read()

    def searchPostalCode(self, searchKey):
        '''우편번호 검색: searchKey 읍/면/동으로 유니코드 입력'''
        action = 'post'
        xml = self._postRequest(action, searchKey)
        soup = BS(xml)
        ret = []
        for item in soup.post.itemlist.findAll('item'):
            ret.append((item.postcd.string, item.address.string))
        return ret

    def tracePackage(self, itemID, lang='ko'):
        '''종추적, EMS 종추적: itemID로 EMS 여부를 자동 판단합니다'''
        itemID = itemID.replace('-', '')
        if itemID.startswith('EM'):
            action = 'ems'
            if lang == 'en':
                action +='Eng'
            action += 'Trace'
        else:
            action = 'trace'
        return self._postRequest(action, itemID)

if __name__ == '__main__':
    APIKEY = '' #여기에 API 키를 넣으세요
    postKr = PostKr(APIKEY)
    print postKr.searchPostalCode('광정동'.decode('utf-8')).decode('euc-kr')
    print postKr.tracePackage('EM123456789KR').decode('euc-kr')

# vim: et sw=4 fenc=utf-8:
