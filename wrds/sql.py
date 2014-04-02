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
        """
            Connect to the sasshare. This will attempt to log in using the provided credentials.
            If it is rejected, the login will try three more times.
        """
        attempt = 0
        self.conn = None
        while attempt < 3 and not self.conn:
            try:
                self.conn = jaydebeapi.connect('com.sas.net.sharenet.ShareNetDrive',
                    ['jdbc:sharenet://wrds-triton.wharton.upenn.edu:8551/', self.username, self.password])
                print "Success"
                return 1
            except:
                print "Your username or password might be incorrect."
                self.username = raw_input('Username: ')
                self.password = getpass.getpass()
                attempt += 1
        print "You were unable to connect. Please contact support."
        return 0

    def get_libraries(self):
        """
            return a list of the libraries in sas.
        """
        cursor = self.conn.cursor()
        cursor.execute('select unique libname from dictionary.tables;')
        return [row[0].strip() for row in cursor.fetchall()]

    def get_tables(self, library, verbose=False):
        """
            returns a list of the datasets in a library.
            If verbose is true: returns a list of dictionaries containing the 
            table name, the number of observations, and the description.
        """
        cursor = self.conn.cursor()
        query = 'select memname, memlabel, nobs from dictionary.tables where libname = "%s";' % library
        cursor.execute(query)
        results = cursor.fetchall()
         
        if verbose:
            output = [{'name': name.strip(), 'desc': label.strip(), 'obs': int(obs)} for name, label, obs in [row for row in results]]
        else:
            output = [name[0].strip() for name in results]

        return output

    def describe_table(self, library, table):
        """
            Takes the library and the table and describes all the columns in that table.
            Includes Column Name, Column Type, Column Length, Column Label, Column Format, Is Null?.
        """
        cursor = self.conn.cursor()
        query = '''select name, type, length, label, format, notnull
                 from dictionary.columns
                 WHERE libname = "{library}" AND memname="{table}";
                 '''
        cursor.execute(query.format(library=library, table=table))
        results = cursor.fetchall()
        output = [{'name': name, 'type': tpe, 'length': length, 'description': label, 'format': formt, 'notnull': notnull}
                    for name, tpe, length, label, formt, notnull in map(lambda s: s.strip(), [entry for entry in results])] 
        return output

    def sql(self, call, df=None, index=None):
        """
            This processes the SQL commands to a Pandas dataframe.
        """
        if df:
            pass
        else:
            return pandas.io.sql.read_sql(call, self.conn, index_col=index)
    

