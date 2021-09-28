WRDS Python Data Access Library
===============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.
The library allows users to access data from WRDS and extract data using SQL statements. The data
that is returned is read into a Pandas data frame.

Installation
~~~~~~~~~~~~

For detailed information on installation of the module, please see `PYTHON: From Your Computer (Jupyter/Spyder) <https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/python-from-your-computer/>`_

Using pip
---------

The easiest way to install WRDS-Py on any supported platform is to use `pip <https://pip.pypa.io/en/stable/quickstart/>`_, the Python package manager, to install from the Python package index (`pypi <https://pypi.org>`_).

``$ pip install wrds``

Windows
-------

WRDS-Py requires the Pandas and Psycopg2 Python packages. Binaries of these can be found here:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg

Once the two required packages are installed, use ``pip`` to install.

Usage
~~~~~

For detailed information on use of the module, please see `Querying WRDS Data using Python <https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/querying-wrds-data-python/>`_

>>> import wrds
>>> db = wrds.Connection()
Enter your credentials.
Username: <your_username>
Password: <your_password>
>>> db.list_libraries()
['audit', 'bank', 'block', 'bvd', 'bvdtrial', 'cboe', ...]
>>> db.list_tables(library='crsp')
['aco_amda', 'aco_imda', 'aco_indfnta', 'aco_indfntq', ...]
>>> db.describe_table(library='crsp', table='stocknames')
Approximately 58957 rows in crsp.stocknames.
       name    nullable              type
0      permno      True  DOUBLE PRECISION      
1      permco      True  DOUBLE PRECISION      
2      namedt      True              DATE
...

>>> stocknames = db.get_table(library='crsp', table='stocknames', obs=10) 
>>> stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS

>>> db.close()  # Close the connection to the database...

>>> with wrds.Connection() as db:  # You can use a context manager
...    stocknames = db.get_table(library='crsp', table='stocknames', obs=10)
>>> stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS
