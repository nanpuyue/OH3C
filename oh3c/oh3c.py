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
    try:
        username = raw_input('Input user name: ')
        password = raw_input('Input password: ')
        device = raw_input('Decice(Press "Enter" to use eth1 as default): ')
        if not device: device = 'eth1'
        macaddr = raw_input('MAC(Press "Enter" if you don\'t need to use binding MAC-address): ')
        if not macaddr: macaddr = 'default'
        return username, password, device, macaddr
    except KeyboardInterrupt:
        print ' Cancel by user !'
        exit()

def prompt_user_name():
    name = raw_input('The user name to delete: ')
    return name

def main():
    # check for root privilege
    if not (os.getuid() == 0):
        print ('Require the permission of root !')
        exit()

    um = usermgr.UserMgr()
    login_info = []
    # test whether user info is empty
    if (um.get_user_number() == 0):
        try:
            choice = raw_input('No user conf file found, creat a new one ?\n<Y/N>: ')
            if choice == 'y' or choice == 'Y': 
                login_info = prompt_user_info()
                um.create_user(login_info)
        except KeyboardInterrupt:
            print ' Cancel by user !'
            exit()
        else: exit()
    else: 
        users_info = um.get_users_info()

        # print menu
        print '\na  Add/Modify user info\nd  Delete a user info\n------'
        for i in range(len(users_info)):
            print i+1, users_info[i]

        while True:
            try:
                choice = raw_input('Your choice(Ctrl + C to cancel): ')
            except KeyboardInterrupt:
                print ' Cancel by user !'
                exit()

            # chioce to add/modify a user
            if (choice == 'a'):
                login_info = prompt_user_info()
                try:
                    um.create_user(login_info)
                    print 'Create the user successfully !'
                except ConfigParser.DuplicateSectionError:
                    um.update_user_info(login_info)
                    print 'Modify the user info successfully !'
                exit()
            
            # chioce to delete a user
            if (choice == 'd'):
                username = prompt_user_name()
                if username in um.get_users_list():
                    um.delete_user(username)
                    print 'Delete user "'+username+'" successfully !'
                    exit()
                else:
                    print 'Not found user named '+username+' !'

            if choice != 'a' and choice != 'd':
                try:
                    login_info =  um.get_user_info(int(choice)-1)
                    break
                except:
                    print 'Please input a valid option !'

    # change mac address for binding mac user
    macaddr = login_info[3]
    if macaddr != 'default':
        line_of_mac = macmgr.get_line_of_mac("'wan'")
        if macaddr not in line_of_mac:
            macmgr.change_mac("'wan'",macaddr)
            macmgr.apply_mac()
    # TODO: delete the following line
    login_info_new = login_info[0:3]
    oh3c = eapauth.EAPAuth(login_info_new)
    oh3c.serve_forever()


if __name__ == "__main__":
    main()
