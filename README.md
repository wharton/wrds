# WRDS-Py from Wharton Research Data Services

WRDS-Py is a Python package for examining datasets on the [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu) platform, and extracting data to Pandas dataframes. A WRDS account is required.

## Installation

The WRDS-Py package is supported on Python 3.8 through 3.12. To ensure you have a supported Python version, type `python --version` at a command line interface, and check that it is between 3.8 and 3.12. On some systems, Python may be in installed as `python3`. You can [download Python here](https://www.python.org/downloads/) if it isn't installed.

The WRDS-Py package must be installed before it can be used for the first time. The recommended method is to use a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) (`venv`), so you can `import` it to use in Python. This example will install the WRDS-Py package (`wrds`) and [IPython](https://ipython.org/), which provides a much nicer command line interface than is included with Python.

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
In [1]: import wrds
In [2]: db = wrds.Connection()
Enter your credentials.
Username: <your_username>
Password: <your_password>
In [3]: db.list_libraries()
['audit', 'bank', 'block', 'bvd', 'bvdtrial', 'cboe', ...]
In [4]: db.list_tables(library="crsp")
['aco_amda', 'aco_imda', 'aco_indfnta', 'aco_indfntq', ...]
In [5]: db.describe_table(library="crsp", table="stocknames")
Approximately 58957 rows in crsp.stocknames.
       name    nullable              type
0      permno      True  DOUBLE PRECISION
1      namedt      True              DATE
2   nameenddt      True              DATE
...

In [6]: stocknames = db.get_table(library="crsp", table="stocknames", rows=10)
In [7]: stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS

In [7]: db.close()  # Close the connection to the database.

In [8]: with wrds.Connection() as db:  # You can use a context manager
   ...:     stocknames = db.get_table(library='crsp', table='stocknames', rows=10)
   ...: stocknames.head()
   permno  permco      namedt   nameenddt     cusip    ncusip ticker  \
0  10000.0  7952.0  1986-01-07  1987-06-11  68391610  68391610  OMFGA
1  10001.0  7953.0  1986-01-09  1993-11-21  36720410  39040610   GFGC
2  10001.0  7953.0  1993-11-22  2008-02-04  36720410  29274A10   EWST
3  10001.0  7953.0  2008-02-05  2009-08-03  36720410  29274A20   EWST
4  10001.0  7953.0  2009-08-04  2009-12-17  36720410  29269V10   EGAS
```
