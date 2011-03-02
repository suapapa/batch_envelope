#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# batch_envelope.py - batch evelope printing script.
#
# Copyright (C) 2011 Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

from PostKr import PostKr
from UnoDocu import UnoDocu

def divideAddress(addr):
    halfLen = (len(addr) - 1) / 2
    atom = addr.split(' ')

    addr1, addr2 = '', ''
    while(atom):
        a1, a2 = '', ''
        try:
            a1 = atom.pop(0)
            a2 = atom.pop()
        except:
            pass
        addr1 = ' '.join((addr1, a1))
        addr2 = ' '.join((a2, addr2))
        if max(len(addr1), len(addr2)) >= halfLen:
            break

    if atom:
        if len(addr1) > len(addr2):
            addr2 = ' '.join(atom + [addr2])
        else:
            addr1 = ' '.join([addr1] + atom)

    return addr1.strip(), addr2.strip()

def formatPostalCode(postcode):
    p1, p2, p3, p4, p5, p6 = postcode
    return '%c %c %c - %c %c %c'%(p1, p2, p3, p4, p5, p6)

def test():
    post = PostKr('5e12d7ed7799470b81298981375429')
    print post.tracePackage('11113-89170122').decode('euc-kr')
    ret =  post.smartSearchPostalCode('경기도 의왕시 포일동 한일나래아파트 201-312'.decode('utf-8'))
    for pc, addr in ret:
        print pc, addr


if __name__ == '__main__':
    from optparse import OptionParser
    optPsr = OptionParser("usage: %prog [-n] GB_dir branch_name manifest_snapshot.xml")
    optPsr.add_option('-a', '--addr', type='string',
                    help="address")
    optPsr.add_option('-n', '--name', type='string',
                    help="name")
    optPsr.add_option('-p', '--phone', type='string',
                    help="phone_number")
    optPsr.add_option('-c', '--postcode', type='string',
                    help="postcode")
    optPsr.add_option('-i', '--cnt', type='string',
                    help="HUMA cnt")
    (opts, args) = optPsr.parse_args()

    post = PostKr('5e12d7ed7799470b81298981375429')
    if opts.postcode:
        ret = post.searchPostalCode(opts.postcode.decode('utf-8'))
        for pc, addr in ret:
            print pc, addr
        exit(0)

    addr = opts.addr.decode('utf-8')
    addr1, addr2 = divideAddress(addr)

    if not opts.postcode:
        # postcode, _addr = post.smartSearchPostalCode(addr)
        ret = post.smartSearchPostalCode(addr)
        if not len(ret) == 1:
            print 'ERR: Ambigious post search result', ret
            exit(-1)
        pCode, _addr = ret[0]
        pCode = formatPostalCode(pCode)
        # print "found postcode %s for addr %s"%(pCode, _addr)

    phoneNumber = ''
    if opts.phone:
        phoneNumber = ' (%s)'%opts.phone

    name = opts.name.decode('utf-8')
    cnt = opts.cnt

    import os
    import time
    os.system('soffice "-accept=socket,host=localhost,port=2002;urp;"')
    time.sleep(1)

    unoDoc = UnoDocu()
    unoDoc.loadTemplate('envelope_templete.odt')

    data = [
        ('$ADDR_LINE1', addr1),
        ('$ADDR_LINE2', addr2),
        ('$POST', pCode),
        ('$NAME', name),
        ('$PHONE', phoneNumber),
        ('$CNT', cnt),
    ]

    for find, replace in data:
        unoDoc.findAndReplace(find, replace)

    unoDoc.sync()
#    unoDoc.save('')
#    unoDoc.close()

    # sometimes, comes up Segmentation fault in shell without this
    time.sleep(1)
    # test()

# vim: et sw=4 fenc=utf-8:
