"""
For additional help, please see https://wrds-web.wharton.upenn.edu/wrds/support/
"""

import jaydebeapi
import os
import pandas as pd
import getpass
from six.moves import configparser
from six.moves import input as _input
import getpass
import platform


class WRDS():

    def sql(self, call, index = None):
        """
        Run a SQL Query on the WRDS Database.

        data = wrds.sql('select * from CRSP.MSI', 'DATE')

        The second argument gives the column name of the index, if you'd like
        your DataFrame to be indexed.
        """

        try:
            return pd.io.sql.read_sql(call, self.CONN, index)
        except Exception as e:
            print('Sorry - this query could not be run.')
            print('Additional information:')
            print(e)

    def _authenticate(self, user, pw):
        try:
            return jaydebeapi.connect('com.sas.net.sharenet.ShareNetDriver', ['jdbc:sharenet://wrds-cloud.wharton.upenn.edu:8551/', user, pw])
        except Exception as e:
            print(e)

    def _parse_config(self, file_location):
        Config = configparser.ConfigParser()

        try:
            Config.read(file_location)
            return Config.get('credentials', 'username'), Config.get('credentials', 'password'), Config.get('credentials', 'classpath')
        except:
            err = 'The .wrdsauthrc file appears to be improperly formatted.\n'
            err += 'Please check the format.\n'
            err += 'The config file needs to appear as below:\n\n'
            err += '[credentials]\n'
            err += 'username=<username>\n'
            err += 'password=<password>\n'
            err += 'classpath=<set of paths to sas.core.jar and sas.intrnet.javatools.jar>\n\n'
            err += 'Please see https://wrds-web.wharton.upenn.edu/wrds/support/ for additional information.\n'
            raise SyntaxError(err)

    def _usage(self):
        if platform.system() == 'Windows':
            home_dir = os.path.expanduser('~'+getpass.getuser())
        else:
            home_dir = os.path.expanduser('~')

        print('Please include a .wrdsauthrc file in your home directory ({}) formatted as below:\n'.format(home_dir))

        err = '[credentials]\n'
        err += 'username=<username>\n'
        err += 'password=<password>\n'
        err += 'classpath=<set of paths to sas.core.jar and sas.intrnet.javatools.jar>\n\n'
        err += 'Please see https://wrds-web.wharton.upenn.edu/wrds/support/ for additional information.\n'
        print(err)

    def is_connected(self):
        ### Add Functionality to determine if connected
        pass

    def _greet_if_interactive(self):
        """
        Check if the user is in an interactive session.

        In the event that the user is in an interactive sesssion, print the welcome message.
        Otherwise, print nothing.

        See https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode for reference.
        """
        import __main__ as main
        if not hasattr(main, '__file__'):
            print('You are now connected with credentials found at {}.'.format(self.AUTHFILE))
            print('\'help(wrds)\' to learn how to interact with the system.')

    def _verify_credentials(self, username, password):
        if self._authenticate(username, password):
            self._greet_if_interactive()
        else:
            err = '\nThe credentials found in {} could not be used to authenticate.\n'.format(self.AUTHFILE)
            err += 'Please verify that the username and password are correct.'
            raise OSError(err)

    def _verify_and_set_classpath(self, classpath, path_delimiter):
        # Classpath should be two paths separated by a colon
        # Try to split on : and check that both paths exist
        paths_to_check = classpath.split(path_delimiter)

        if paths_to_check == ['']: # The user may have not included any paths in the classpath section
            err = '\nPlease specify paths for the JDBC drivers in the classpath section of {}'.format(AUTHFILE)
            raise SyntaxError(err)

        for path in paths_to_check:
            if not os.path.exists(path):
                err = '\nCould not the driver specified at {}\n'.format(path)
                err += 'Please check that classpath is set correctly in {}.'.format(self.AUTHFILE)
                raise SystemError(err)

        # If classpaths exist, set the appropriate environment variable
        os.environ['CLASSPATH'] = classpath

    def _verify_classpath_and_credentials(self, config_settings):
        if platform.system() == 'Windows':
            classpath_delimiter = ';'
        else:
            classpath_delimiter = ':'

        username, password, classpath = config_settings
        self._verify_and_set_classpath(classpath, classpath_delimiter)
        self._verify_credentials(username, password)

    def __init__(self, username=None, password=None, classpath=None):

        if all( i == None for i in (username, password, classpath)):
            # No Inputs specified, check for file and then bow out
            self.CONN = None
            if platform.system() == 'Windows':
                self.AUTHFILE = os.path.join(os.path.expanduser('~'+getpass.getuser()), '.wrdsauthrc')

            else:
                self.AUTHFILE = os.path.join(os.path.expanduser('~'), '.wrdsauthrc')

            if os.path.isfile(self.AUTHFILE):
                self._verify_classpath_and_credentials(self._parse_config(self.AUTHFILE))
                username, password, _ = self._parse_config(self.AUTHFILE)
                self.CONN = self._authenticate(username, password)
            else:
                self._usage()
        elif all(i != None for i in (username, password, classpath)):
            ### All three specified
            pass

        else:
            #### Something horrible happened'
            pass