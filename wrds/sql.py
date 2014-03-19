# -*- coding: utf-8 -*-

import os
import getpass

import jaydebeapi
import pandas

class SQLConnection(object):
    def __init__(self):
        print "Enter your credentials."
        self.username = raw_input("Username: ")
        self.password = getpass.getpass()
        try:
            self.conn = jaydebeapi.connect('com.sas.net.sharenet.ShareNetDrive',
                ['jdbc:sharenet//wrds-triton.wharton.upenn.edu:8551/', self.username, self.password])
        except:
            print "Your username or password might be incorrect."
    

