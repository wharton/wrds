# -*- coding: utf-8 -*-

import os
import getpass

import jaydebeapi
import pandas

class SQLConnection(object):
    def __init__(self, username=None, password=None):
        if not username and not password:
            print "Enter your credentials."
            self.username = raw_input("Username: ")
            self.password = getpass.getpass()
        else:
            self.username = username
            self.password = password
    
    def connnect(self):
        try:
            self.conn = jaydebeapi.connect('com.sas.net.sharenet.ShareNetDrive',
                ['jdbc:sharenet//wrds-triton.wharton.upenn.edu:8551/', self.username, self.password])
        except:
            print "Your username or password might be incorrect."

    def sql(call, df=None, index=None):
        if df:
            pass
        else:
            return pandas.io.sql.read_sql(call, self.conn, index_col=index)
    

