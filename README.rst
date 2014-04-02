WRDS Python Data Access Library
==============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.

    >>> import wrds
    >>> data = wrds.sql('select * from Crsp.msi', index='DATE')
    >>> data.head()

There will be more added to this, including additional data processing methods.

"""


