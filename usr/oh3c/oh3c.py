#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Main program for oh3c.

"""

__version__ = '0.2'

import os, sys
import ConfigParser
from socket import *

import eapauth
import usermgr
import macmgr
           
def prompt_user_info():
    name = raw_input('Input user name:')
    password = raw_input('Input password:')
    dev = raw_input('Decice(eth1 by default): ')
    if not dev: dev = 'eth1'
    macaddr = raw_input('MAC:(no input for no change):')
    if not macaddr: macaddr = 'default'
    return name, password, dev,macaddr

def main():
    # check for root privilege
    if not (os.getuid() == 0):
        print ('Require the permission of root!')
        exit(-1)

    um = usermgr.usermgr()
    login_info = []
    if (um.get_user_number() == 0):
        choice = raw_input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y': 
            login_info = prompt_user_info()
            um.create_user(login_info)
        else: exit(-1)
    else: 
        users_info = um.get_users_info()

        print '0. Add a new user'
        for i in range(len(users_info)):
            print i+1, users_info[i]

        while True:
            try:
                choice = int(raw_input('Your choice: '))
            except ValueError:
                print 'Please input a valid number!'
            else: break;
        if (choice == 0):
            try:
                login_info = prompt_user_info()
                um.create_user(login_info)
            except ConfigParser.DuplicateSectionError:
                print 'user already exist!'
        else: login_info =  um.get_user_info(choice-1)
    macaddr = login_info[3]
    line_of_mac = macmgr.get_line_of_mac("'wan'")
    if macaddr not in line_of_mac and macaddr != 'default':
        macmgr.change_mac("'wan'",macaddr)
        macmgr.apply_mac()
    login_info_new = login_info[0:3]
    oh3c = eapauth.EAPAuth(login_info_new)
    oh3c.serve_forever()


if __name__ == "__main__":
    main()
