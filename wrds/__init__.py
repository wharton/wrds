# -*- coding: utf-8 -*-

"""
WRDS Python Data Access Library
==============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.

    >>> import wrds
    >>> db = wrds.Connection()
    >>> db.list_libraries()
    ['aha', 'aha_sample', 'ahasamp', 'audit', 'audit_audit_comp', ...]
    >>> db.list_tables(library='crsp')
    ['acti', 'asia', 'asib', 'asic', 'asio', 'asix', 'bmdebt', 'bmheader', ...]
    >>> data = db.raw_sql('SELECT * FROM crsp.stocknames', index_col='permno')
    >>> data.head()
             permco      namedt   nameenddt     cusip    ncusip ticker  \
    permno
    10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
    10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
    10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
    10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
    10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS
    ...
"""
from wrds._version import __version__
from datetime import date

__title__ = "wrds-py"
__author__ = "Wharton Research Data Services"
__copyright__ = f"2017 - {date.today().year} Wharton Research Data Services"

from .sql import Connection
