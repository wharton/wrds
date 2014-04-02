# -*- coding: utf-8 -*-

"""
WRDS Python Data Access Library
==============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.

    >>> import wrds
    >>> connection = wrds.SQLConnection(username='user', password='password') 
    >>> connection.get_libraries()
    >>> connection.get_tables('CRSP', verbose=True)
    >>> data = connection.sql('SELECT * FROM CRSP.MSI', index='DATE')
    >>> data.head()


"""

__title__ = 'wrds-py'
__version__ = '0.1.0'
__author__ = 'Eric Stein'
__copyright__ = '2014 Wharton Research Data Services'

import os

from .sql import SQLConnection


# set up the Java environment for the odbc drivers.
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java'
os.environ['CLASSPATH'] = '/usr/local/etc/sas_jdbc_driver/sas.core.jar:/usr/local/etc/sas_jdbc_driver/sas.intrnet.javatools.jar'
