# -*- coding: utf-8 -*-
import getpass

import jaydebeapi
import pandas
#import sqlparse

class SQLConnection(object):
    def __init__(self, username=None, password=None):
        if not username and not password:
            print "Enter your credentials."
            self.username = raw_input("Username: ")
            self.password = getpass.getpass()
        else:
            self.username = username
            self.password = password
    
    def connect(self):
        """
            Connect to the sasshare. This will attempt to log in using the provided credentials.
            If it is rejected, the login will try three more times.
        """
        attempt = 0
        self.conn = None
        while attempt < 3 and not self.conn:
            try:
                self.conn = jaydebeapi.connect('com.sas.net.sharenet.ShareNetDriver',
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
            data = [{'name': name.strip(), 'desc': label.strip(), 'obs': float(obs)} for name, label, obs in [row for row in results]]
            output = {}
            for item in data:
                output[item.pop('name')] = item
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

        data = [{'name': name, 'type': tpe, 'length': float(length), 'description': label, 'format': formt, 'notnull': notnull}
                    for name, tpe, length, label, formt, notnull in [map(lambda s: str(s).strip(), e) for e in results]] 
        output = {}
        for item in data:
            output[item.pop('name')] = item

        return output


#    def _get_library_and_table(sql):
#        parsed = sqlparse.parse(sql)
#        query = parsed[0]
#        struct = list(query.get_sublists())
#        columns = [c.normalized for c in struct[0].get_sublists()]
#        library = struct[1].get_parent_name().upper()
#        table = struct[1].get_name().upper()
#        return columns, library, table
#
    def sql(self, call, index=None, metadata=False):
        """
            This processes the SQL commands to a Pandas dataframe.
        """
        df =  pandas.io.sql.read_sql(call, self.conn, index_col=index)

        #if metadata:
        #    columns, library, table = self._get_library_and_table(call)
        #    desc = self.describe_table(library=library, table=table)
        #    for a in [m for m in dir(df) if m in desc.keys()]:
        #        df.__getattr__(a).__dict__ = df.__getattr__(a).__dict__.update(desc[a])
        return df 

