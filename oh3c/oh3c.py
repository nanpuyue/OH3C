#!/usr/bin/python
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
    dev = raw_input('Decice(Press "Enter" to use eth1 as default): ')
    if not dev: dev = 'eth1'
    macaddr = raw_input('MAC(Press "Enter" if you don\'t need to use binding MAC-address): ')
    if not macaddr: macaddr = 'default'
    return name, password, dev, macaddr

def main():
    # check for root privilege
    if not (os.getuid() == 0):
        print ('Require the permission of root!')
        exit(-1)

    um = usermgr.UserMgr()
    login_info = []
    # test whether user info is empty
    if (um.get_user_number() == 0):
        choice = raw_input('No user conf file found, creat a new one?\n<Y/N>: ')
        if choice == 'y' or choice == 'Y': 
            login_info = prompt_user_info()
            um.create_user(login_info)
        else: exit(-1)
    else: 
        users_info = um.get_users_info()

        # print menu
        print '0. Create/Modify user info'
        for i in range(len(users_info)):
            print i+1, users_info[i]

        while True:
            try:
                choice = int(raw_input('Your choice: '))
            except ValueError:
                print 'Please input a valid number!'
            else: break;
        # chioce to add/modify a user
        if (choice == 0):
            login_info = prompt_user_info()
            try:
                um.create_user(login_info)
                print 'Create user info Successfully!'
            except ConfigParser.DuplicateSectionError:
                um.update_user_info(login_info)
                print 'Update user info Successfully!'
        else: login_info =  um.get_user_info(choice-1)

    # change mac address for binding mac user
    macaddr = login_info[3]
    line_of_mac = macmgr.get_line_of_mac("'wan'")
    if macaddr not in line_of_mac and macaddr != 'default':
        macmgr.change_mac("'wan'",macaddr)
        macmgr.apply_mac()
    #TODO: delete the following line 
    login_info_new = login_info[0:3]
    oh3c = eapauth.EAPAuth(login_info_new)
    oh3c.serve_forever()


if __name__ == "__main__":
    main()
