# -*- coding: utf-8 -*-
import getpass

import pandas as pd
import sqlalchemy as sa
import prettytable

class Connection(object):
    def __init__(self, username=None, password=None):
        if not username and not password:
            print("Enter your credentials.")
            if not username:
                username = getpass.getuser()
                _ = input("Username ({}): ".format(username))
                if _:
                    username = _
            self.username = username
            if not password:
                password = getpass.getpass('Enter your password:')
        else:
            self.username = username
        self.engine = sa.create_engine('postgresql://{usr}:{pwd}@wrds-pgdata1-h/wrds'.format(usr=self.username, pwd=password)) 
        try:
            self.engine.connect()
            self.insp = sa.inspect(self.engine)
        except:
            print("Error logging in. Try your username and password again")
    
    def get_libraries(self):
        """
            Use inspection to return all schemas   
        """
        for schema in self.insp.get_schema_names():
            print(schema)

    def get_tables(self, library, verbose=False):
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

    def raw_sql(self, sql, coerce_float=True, date_cols=None):
        """
            This processes the SQL commands to a Pandas dataframe.
        """
        return pd.read_sql_query(sql, self.engine, coerce_float=coerce_float, parse_dates=date_cols)

    def get_table(self, library, table, columns=None, index_col=None, date_cols=None):
        """
            Return an entire table from the database
        """
        return pd.read_sql_table(table, self.engine, schema=library, columns=columns, index_col=index_col, parse_dates=date_cols)

