WRDS Python Data Access Library
==============================

WRDS-Py is a library for extracting data from WRDS data sources and getting it into Pandas.
The library allows users to access SAS/SHARE and extract data using SQL statements. The data
that is returned is read into a Pandas data frame.

Usage
~~~~~

>>> import wrds
>>> connection = wrds.SQLConnecion()
Enter your credentials.
Username: <your_username>
Password: <your_password>
>>>connection.connect()
Success
>>> connection.get_libraries()
['AUDIT', 'BANK', 'BLOCK', 'BVD', 'BVDTRIAL', 'CBOE', ...]
>>> connection.get_tables('COMP')
['ACO_AMDA', 'ACO_IMDA', 'ACO_INDFNTA', 'ACO_INDFNTQ', ...]
>>> connection.describe_table('COMP', 'ACO_AMDA')
{'consol': {'description': 'Level of Consolidation', format': '$2.', ...}
>>> df = connection.sql('SELECT * FROM COMP.ACO_IMDA')
>>> df.head()
    gvkey        indfmt consol popsrc  fyr       datafmt  sequencen  \
    0  001004  INDL             C       D    5  STD                   1
    1  001013  INDL             C       D   10  STD                   1
    2  001013  INDL             C       D   10  STD                   1
    3  001034  INDL             C       D   12  STD                   1
    4  001045  INDL             C       D   12  STD                   1

                                                    note  \
                                                    0  per nw As previously announced, during the thi...
                                                    1  (Nt 3) Acquistion of LGC Wireless Inc on Decem...
                                                    2  MINNEAPOLIS--(BUSINESS WIRE)--November 19, 200...
                                                    3  Per Note 3, " Sale of the API Business - On Fe...
                                                    4  Per Item 2 (MDA), "The Company recorded a net ...

                                                                             notetype                         subtype    datadate
                                                                             0  FUNDAMENTAL                     DISC OPS                        2011-02-28
                                                                             1  FUNDAMENTAL                     ACQUISITION                     2008-07-31
                                                                             2  FUNDAMENTAL                     FISCAL YEAR CHANGE              2009-10-31
                                                                             3  FUNDAMENTAL                     DISC OPS                        2008-03-31
                                                                             4  FUNDAMENTAL                     MANAGEMENT DISCUSSION           2008-03-31

                                                                             [5 rows x 11 columns]
