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

    def get_libraries(self):
        """
            return a list of the libraries in sas.
        """
        cursor = self.conn.cursor()
        cursor.execute('select unique libname from dictionar.tables;')
        return [row[0].strip() for row in cursor.fetchall()]

    def get_tables(self, library, verbose=False):
        """
            returns a list of the datasets in a library.
            If verbose is true: returns a list of dictionaries containing the 
            table name, the number of observations, and the desciprtion.
        """
        cursor = self.conn.cursor()
        query = 'select memname, memlabel, nobs from dictionary.tables where libname = %s' % library
        cursor.execute(query)
        if verbose:
            output = [{'name': name.strip(), 'desc': label.strip(), 'obs': int(obs)} for name, label, obs in cursor.fetchall()]
        else:
            output = [name[0].strip() for name in cursor.fetchall()]

        return output


    def sql(self, all, df=None, index=None):
        if df:
            pass
        else:
            return pandas.io.sql.read_sql(call, self.conn, index_col=index)
    

