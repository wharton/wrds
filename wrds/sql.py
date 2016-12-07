# -*- coding: utf-8 -*-
import getpass
import warnings

import pandas as pd
import sqlalchemy as sa
import prettytable

from sys import version_info
py3 = version_info[0] > 2

if not py3:
    input = raw_input

class Connection(object):
    def __init__(self):
        self.engine = sa.create_engine('postgresql://wrds-pgdata2.wharton.upenn.edu:9737/wrds') 
        try:
            self.engine.connect()
            self.insp = sa.inspect(self.engine)
        except Exception as e:
            uname = getpass.getuser()
            username = input("Enter your username [{}]:".format(uname))
            if not username:
                username = uname
            passwd = getpass.getpass('Enter your password:')
            self.engine = sa.create_engine('postgresql://{usr}:{pwd}@wrds-pgdata2.wharton.upenn.edu:9737/wrds'.format(usr=username, pwd=passwd)) 
            warnings.warn("WRDS recommends setting up a .pgpass file. You can find more info here: https://www.postgresql.org/docs/9.2/static/libpq-pgpass.html")
    
    def list_libraries(self):
        """
            Use inspection to return all schemas   
        """
        for schema in self.insp.get_schema_names():
            print(schema)

    def list_tables(self, library, verbose=False):
        """
            returns a list of the datasets in a library.
            If verbose is true: returns a list of dictionaries containing the 
            table name, the number of observations, and the description.
        """
        for table in self.insp.get_table_names(schema=library):
            print(table)

    def describe_table(self, library, table):
        """
            Takes the library and the table and describes all the columns in that table.
            Includes Column Name, Column Type, Nullable?.
        """
        output = prettytable.PrettyTable(["Name", "Type", "Nullable"])
        for row in self.insp.get_columns(table, schema=library):
            output.add_row([row['name'], row['type'], row['nullable']])
        print(output)

    def raw_sql(self, sql, coerce_float=True, date_cols=None, index_col=None):
        """
            This processes the SQL commands to a Pandas dataframe.
        """
        return pd.read_sql_query(sql, self.engine, coerce_float=coerce_float, parse_dates=date_cols, index_col=index_col)

    def get_table(self, library, table, columns=None, coerce_float=None, index_col=None, date_cols=None, obs=-1):
        """
            Return an entire table from the database
        """
        if obs == -1:
            obsstmt = ''
        else:
            obsstmt = ' LIMIT {}'.format(obs)
        if columns is None:
            cols = '*'
        else:
            cols = ','.join(columns)
        sqlstmt = 'select {cols} from {schema}.{table} {obsstmt};'.format(cols=cols, schema=library, table=table, obsstmt=obsstmt)
        return self.raw_sql(sqlstmt, coerce_float=coerce_float, index_col=index_col, date_cols=date_cols)
