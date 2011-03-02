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

if __name__ == '__main__':
    from optparse import OptionParser
    optPsr = OptionParser("usage: %prog [-n] GB_dir branch_name manifest_snapshot.xml")
    optPsr.add_option('-n', '--dryrun', action='store_true', default=False,
                    help="just print patch list")
    optPsr.add_option('-e', '--exclude', type='string',
                    help="exclude these patches. use \",\" to give many numbers")
    optPsr.add_option('-s', '--skipsync', action='store_true', default=False,
                    help="don't do repo sync")
    (opts, args) = optPsr.parse_args()

    post = PostKr('5e12d7ed7799470b81298981375429')
    ret = post.searchPostalCode('서울시립대학교'.decode('utf-8'))
    for pc, addr in ret:
        print pc, addr

    print post.tracePackage('11113-89170122').decode('euc-kr')

# vim: et sw=4 fenc=utf-8:
