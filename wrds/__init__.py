import jaydebeapi
import os
import pandas as pd
import getpass
from six.moves import configparser, input

AUTHFILE = os.path.join(os.path.expanduser('~'), '.wrdsauthrc')

def sql(call, index = None):
    """
    Run a SQL Query on the WRDS Database.

    data = wrds.sql('select * from CRSP.MSI', 'DATE')
    
    The second argument gives the column name of the index, if you'd like
    your DataFrame to be indexed.
    """
   
    try:
        return pd.io.sql.read_sql(call, conn, index)
    except Exception as e:
        print('Sorry - this query could not be run.')
        print('Additional information:')
        print(e)

def _authenticate(user, pw):
    global conn

    try:
        conn = jaydebeapi.connect('com.sas.net.sharenet.ShareNetDriver', ['jdbc:sharenet://wrds-cloud.wharton.upenn.edu:8551/', user, pw])
    except Exception as e:
        print(e)
        conn = None

    return conn

def _parse_config(file_location):
    Config = configparser.ConfigParser()

    try:
        Config.read(file_location)
        result = Config.get('credentials', 'username'), Config.get('credentials', 'password'), Config.get('credentials', 'classpath')
    except:
        err = 'The .wrdsauthrc file appears to be improperly formatted.\n'
        err += 'Please check the format.\n'
        err += 'The config file needs to appear as below, where <username> and <password> are replaced with your username and password, respectively.\n\n'
        err += '[credentials]\n'
        err += 'username=<username>\n'
        err += 'password=<password>\n'
        err += 'classpath=<set of paths to sas.core.jar and sas.intrnet.javatools.jar>\n\n'
        err += 'Please see https://wrds-web.wharton.upenn.edu/wrds/support/ for additional information.\n'
        
        print(err)
        return False
    return result

def _welcome():
    print('Did not find a .wrdsauthrc file in your home directory.')
    print('Please enter your credentials manually.\n')

def _manual_connect():
    username = input('Username: ')
    password = getpass.getpass()

    conn = _authenticate(username, password)

    while conn == None:
        username = input('Username: ')
        password = getpass.getpass()
        conn = _authenticate(username, password)

    print('You are now connected. \'help(wrds)\' to learn how to interact with the system.')

def _greet_if_interactive():
    """ 
    Check if the user is in an interactive session.

    In the event that the user is in an interactive sesssion, print the welcome message.
    Otherwise, print nothing.

    See https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode for reference.
    """
    import __main__ as main
    if not hasattr(main, '__file__'):
        print('You are now connected with credentials found at ' + AUTHFILE + '.')
        print('\'help(wrds)\' to learn how to interact with the system.')
    
if os.path.isfile(AUTHFILE):
    credentials = _parse_config(AUTHFILE)
    if credentials: 
        username, password, classpath = credentials
        os.environ['CLASSPATH'] = classpath
        if _authenticate(username, password):
            _greet_if_interactive()
        else:
            print('The credentials found in ' + AUTHFILE + ' could not be used to authenticate.')
            print('Please provide your username and password.')
            _manual_connect()
else:
    _welcome()
    _manual_connect()

