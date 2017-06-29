# -*- coding: utf-8 -*-
import getpass
import warnings

import pandas as pd
import sqlalchemy as sa

from sys import version_info
py3 = version_info[0] > 2

if not py3:
    input = raw_input  # use raw_input in python 2

class NotSubscribedError(PermissionError):
    pass

class SchemaNotFoundError(FileNotFoundError):
    pass

class Connection(object):
    def __init__(self):
        """
        Establish the connection to the database. This will use the .pgpass file if the user has set one up. If not,
        it will ask the user for a username and password. It will also direct the user to information on setting up
        .pgpass

        Additionally, creating the instance will load a list of schemas the user has permission to access.

        :return: None

        Usage::
        >>> db = wrds.Connection()
        Loading library list...
        Done
        """
        self.engine = sa.create_engine('postgresql://wrds-pgdata.wharton.upenn.edu:9737/wrds', connect_args={'sslmode': 'require'}) 
        try:
            self.engine.connect()
        except Exception as e:
            uname = getpass.getuser()
            username = input("Enter your WRDS username [{}]:".format(uname))
            if not username:
                username = uname
            passwd = getpass.getpass('Enter your password:')
            pghost = 'postgresql://{usr}:{pwd}@wrds-pgdata.wharton.upenn.edu:9737/wrds'
            self.engine = sa.create_engine(pghost.format(
                usr=username, pwd=passwd), connect_args={'sslmode':'require'})
            warnings.warn("WRDS recommends setting up a .pgpass file. You can find more info here: https://www.postgresql.org/docs/9.2/static/libpq-pgpass.html.")
            try:
                self.engine.connect()
            except Exception as e:
                print("There was an error with your password.")
                raise e

        self.insp = sa.inspect(self.engine)
        print("Loading library list...")
        query = """
        WITH RECURSIVE "names"("name") AS (
        SELECT n.nspname AS "name"
        FROM pg_catalog.pg_namespace n
        WHERE n.nspname !~ '^pg_'
        AND n.nspname <> 'information_schema'
        ) SELECT "name"
        from "names"
        where pg_catalog.has_schema_privilege(current_user, "name", 'USAGE') = TRUE
        ;
        """
        cursor = self.engine.execute(query)
        self.schema_perm = [x[0] for x in cursor.fetchall() if not (x[0].endswith('_old') or x[0].endswith('_all'))]
        print("Done")

    def __check_schema_perms(self, schema):
        """
            Check the permissions of the schema. Raise permissions error if user does not have
            access. Raise other error if the schema does not exist.

            Else, return True
            
            :param schema: Postgres schema name.
            :rtype: bool
            
        """
        
        if schema in self.schema_perm:
            return True
        else:
            if schema in self.insp.get_schema_names():
                raise NotSubscribedError("You do not have permission to access the {} library".format(schema))
            else:
                raise SchemaNotFoundError("The {} library is not found.".format(schema)) 
    
    def list_libraries(self):
        """
            Return all the libraries (schemas) the user can access.

            :rtype: list

            Usage::
            >>> db.list_libraries()
            ['aha', 'audit', 'block', 'boardex', ...]
        """
        return self.schema_perm

    def list_tables(self, library):
        """
            Returns a list of all the tables within a schema.

            :param library: Postgres schema name.

            :rtype: list

            Usage::
            >>> db.list_tables('wrdssec')
            ['wciklink_gvkey', 'dforms', 'wciklink_cusip', 'wrds_forms', ...]
        """
        if self.__check_schema_perms(library):
            return self.insp.get_view_names(schema=library)

    def __get_schema_for_view(self, schema, table):
        """
        Internal function for getting the schema based on a view
        """
        sql_code = """SELECT distinct(source_ns.nspname) as source_schema
                      FROM pg_depend
                      JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid
                      JOIN pg_class as dependent_view ON pg_rewrite.ev_class = dependent_view.oid
                      JOIN pg_class as source_table ON pg_depend.refobjid = source_table.oid
                      JOIN pg_attribute ON pg_depend.refobjid = pg_attribute.attrelid
                      AND pg_depend.refobjsubid = pg_attribute.attnum
                      JOIN pg_namespace dependent_ns ON dependent_ns.oid = dependent_view.relnamespace
                      JOIN pg_namespace source_ns ON source_ns.oid = source_table.relnamespace
                      where dependent_ns.nspname = '{schema}' and dependent_view.relname = '{view}';
                    """.format(schema=schema, view=table)
        if self.__check_schema_perms(schema):
            result = self.engine.execute(sql_code)
            return result.fetchone()[0]

    def describe_table(self, library, table):
        """
            Takes the library and the table and describes all the columns in that table.
            Includes Column Name, Column Type, Nullable?.

            :param library: Postgres schema name.
            :param table: Postgres table name.

            :rtype: pandas.DataFrame

            Usage::
            >>> db.describe_table('wrdssec_all', 'dforms')
                        name nullable     type
                  0      cik     True  VARCHAR
                  1    fdate     True     DATE
                  2  secdate     True     DATE
                  3     form     True  VARCHAR
                  4   coname     True  VARCHAR
                  5    fname     True  VARCHAR
        """
        rows = self.get_row_count(library, table)
        print("Approximately {} rows in {}.{}.".format(rows, library, table))
        table_info = pd.DataFrame.from_dict(self.insp.get_columns(table, schema=library))
        return table_info[['name', 'nullable', 'type']]

    def get_row_count(self, library, table):
        """
            Uses the library and table to get the approximate row count for the table. 
            
            :param library: Postgres schema name.
            :param table: Postgres table name.

            :rtype: int
    
            Usage::
            >>> db.get_row_count('wrdssec', 'dforms')
            16378400
        """
        schema = self.__get_schema_for_view(library, table)
        if schema: 
            sqlstmt = """
                select reltuples from pg_class r JOIN pg_namespace n on (r.relnamespace = n.oid)
                where r.relkind = 'r' and n.nspname = '{}' and r.relname = '{}';
                """.format(schema, table)

            try:
                result = self.engine.execute(sqlstmt)
                return int(result.fetchone()[0])
            except Exception as e:
                print("There was a problem with retrieving the row count: {}".format(e))
                return 0
        else:
            print("There was a problem with retrieving the schema")
            return None

    def raw_sql(self, sql, coerce_float=True, date_cols=None, index_col=None):
        """
            Queries the database using a raw SQL string.

            :param sql: SQL code in string object.
            :param coerce_float: (optional) boolean, default: True
                Attempt to convert values to non-string, non-numeric objects
                to floating point. Can result in loss of precision.
            :param date_cols: (optional) list or dict, default: None
                - List of column names to parse as date
                - Dict of ``{column_name: format string}`` where format string is
                  strftime compatible in case of parsing string times or is one of
                  (D, s, ns, ms, us) in case of parsing integer timestamps
                - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
                  to the keyword arguments of :func:`pandas.to_datetime`
            :param index_col: (optional) string or list of strings, default: None
                Column(s) to set as index(MultiIndex)

            :rtype: pandas.DataFrame

            Usage ::
            >>> data = db.raw_sql('select cik, fdate, coname from wrdssec_all.dforms;', date_cols=['fdate'], index_col='cik')
            >>> data.head()
                cik        fdate       coname
                0000000003 1995-02-15  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1996-02-14  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1997-02-19  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1998-03-02  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1998-03-10  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y..
                ...
        """
        try:
            return pd.read_sql_query(sql, self.engine, coerce_float=coerce_float, parse_dates=date_cols, index_col=index_col)
        except sa.exc.ProgrammingError as e:
            raise e

    def get_table(self, library, table, obs=-1, offset=0, columns=None, coerce_float=None, index_col=None, date_cols=None):
        """
            Creates a data frame from an entire table in the database.

            :param sql: SQL code in string object.
            :param library: Postgres schema name.

            :param obs: (optional) int, default: -1
                Specifies the number of observations to pull from the table. An integer
                less than 0 will return the entire table.
            :param offset: (optional) int, default: 0
                Specifies the starting point for the query. An offset of 0 will start
                selecting from the beginning.
            :param columns: (optional) list or tuple, default: None
                Specifies the columns to be included in the output data frame.
            :param coerce_float: (optional) boolean, default: True
                Attempt to convert values to non-string, non-numeric objects
                to floating point. Can result in loss of precision.
            :param date_cols: (optional) list or dict, default: None
                - List of column names to parse as date
                - Dict of ``{column_name: format string}`` where format string is
                  strftime compatible in case of parsing string times or is one of
                  (D, s, ns, ms, us) in case of parsing integer timestamps
                - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
                  to the keyword arguments of :func:`pandas.to_datetime`
            :param index_col: (optional) string or list of strings, default: None
                Column(s) to set as index(MultiIndex)

            :rtype: pandas.DataFrame

            Usage ::
            >>> data = db.get_table('wrdssec_all', 'dforms', obs=1000, columns=['cik', 'fdate', 'coname'])
            >>> data.head()
                cik        fdate       coname
                0000000003 1995-02-15  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1996-02-14  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1997-02-19  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1998-03-02  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y...
                0000000003 1998-03-10  DEFINED ASSET FUNDS MUNICIPAL INVT TR FD NEW Y..
                ...

        """
        if obs < 0:
            obsstmt = ''
        else:
            obsstmt = ' LIMIT {}'.format(obs)
        if columns is None:
            cols = '*'
        else:
            cols = ','.join(columns)
        if self.__check_schema_perms(library):
            sqlstmt = 'select {cols} from {schema}.{table} {obsstmt} OFFSET {offset};'.format(cols=cols, schema=library,
                    table=table, obsstmt=obsstmt, offset=offset)
            return self.raw_sql(sqlstmt, coerce_float=coerce_float, index_col=index_col, date_cols=date_cols)
