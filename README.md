# WRDS Python Data Access Library

WRDS-Py is a Python package for examining datasets on the [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu) platform, and extracting it to Pandas dataframes. A WRDS account is required.

## Installation

Before installing the WRDS-Py package, make sure you have a supported version of Python. At a command line interface, type `python --version`, and make sure it is 3.8 or higher.

The WRDS-Py package must be installed before it can be used for the first time. The best way to do this is to use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), or `venv`, so you can `import` it to use in Python. In this example, we will show the a Linux prompt (`$`), This example will also [install IPython](https://ipython.org/), which provides a nice command-line interface.

#### Linux or MacOS

```
$ python -m venv --copies --prompt wrds-py wrds-py
$ source wrds-py/bin/activate
(wrds-py) $ python -m pip install -U pip wheel wrds ipython
```

In this example, Python will create a `venv` in your current directory `./wrds-py`, so that when you want to use it again, you can simply activate it:

```
$ source wrds-py/bin/activate
```

#### Windows

```
C:\Users\username> python -m venv --copies --prompt wrds-py wrds-py
C:\Users\username> wrds-py\Scripts\activate
(wrds-py) C:\Users\username> python -m pip install -U pip wheel wrds ipython
```

In this example, Python will create a `venv` in the directory `C:\Users\username\wrds-py`, so that when you want to use it again, you can simply activate it:

```
C:\Users\username> wrds-py\Scripts\activate
```

For detailed information on installation of the module, please see [PYTHON: From Your Computer (Jupyter/Spyder)](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/python-from-your-computer/)

## Using the Py-WRDS Package

Type `ipython` to start the IPython command line interface.

For detailed information on use of the module, please see [Querying WRDS Data using Python](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-python/querying-wrds-data-python/)

A quick tutorial:

```
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

>>> stocknames = db.get_table(library='crsp', table='stocknames', rows=10) 
>>> stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS

>>> db.close()  # Close the connection to the database...

>>> with wrds.Connection() as db:  # You can use a context manager
...    stocknames = db.get_table(library='crsp', table='stocknames', rows=10)
>>> stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS
```
