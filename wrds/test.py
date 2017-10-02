# -*- coding: utf-8 -*-

import wrds
import unittest
try:
    import unittest.mock as mock
except ImportError:
    from mock import mock
import sys

class TestInitMethod(unittest.TestCase):
    """ Test the wrds.Connection.__init__() method,
        with both default and custom parameters.
    """
    @mock.patch('wrds.sql.sa')
    def test_init_calls_sqlalchemy_create_engine_defaults(self, mock_sa):
        t = wrds.Connection()
        connstring = 'postgresql://{host}:{port}/{dbname}'
        connstring = connstring.format(
            host=wrds.sql.WRDS_POSTGRES_HOST,
            port=wrds.sql.WRDS_POSTGRES_PORT,
            dbname=wrds.sql.WRDS_POSTGRES_DB)
        mock_sa.create_engine.assert_called_with(
            connstring,
            connect_args={'sslmode': 'require'})

    @mock.patch('wrds.sql.sa')
    def test_init_calls_sqlalchemy_create_engine_custom(self, mock_sa):
        username = 'faketestusername'
        connstring = 'postgresql://{usr}@{host}:{port}/{dbname}'
        connstring = connstring.format(
            usr=username,
            host=wrds.sql.WRDS_POSTGRES_HOST,
            port=wrds.sql.WRDS_POSTGRES_PORT,
            dbname=wrds.sql.WRDS_POSTGRES_DB)
        t = wrds.Connection(wrds_username=username)
        mock_sa.create_engine.assert_called_with(
            connstring,
            connect_args={'sslmode': 'require'})

    @mock.patch('wrds.sql.Connection.load_library_list')
    @mock.patch('wrds.sql.Connection.connect')
    def test_init_default_connect(self, mock_connect, mock_lll):
        t = wrds.Connection()
        mock_connect.assert_called_once()

    @mock.patch('wrds.sql.Connection.connect')
    def test_init_autoconnect_false_no_connect(self, mock_connect):
        t = wrds.Connection(autoconnect=False)
        mock_connect.assert_not_called()

    @mock.patch('wrds.sql.Connection.connect')
    @mock.patch('wrds.sql.Connection.load_library_list')
    def test_init_default_load_library_list(self, mock_lll, mock_connect):
        t = wrds.Connection()
        mock_lll.assert_called_once()

    @mock.patch('wrds.sql.Connection.connect')
    @mock.patch('wrds.sql.Connection.load_library_list')
    def test_init_autoconnect_false_no_connect(self, mock_lll, mock_connect):
        t = wrds.Connection(autoconnect=False)
        mock_lll.assert_not_called()


class TestConnectMethod(unittest.TestCase):
    """ Test the wrds.Connection.connect method.

        Since all exceptions are caught immediately,
        I'm just not smart enough to simulate bad passwords with
        the code as written.
    """
    def setUp(self):
        self.t = wrds.Connection(autoconnect=False)
        self.t._hostname = 'wrds.test.private'
        self.t._port = 12345
        self.t._username = 'faketestusername'
        self.t._password = 'faketestuserpass'
        self.t._dbname = 'testdbname'
        self.t._Connection__get_user_credentials = mock.Mock()
        self.t._Connection__get_user_credentials.return_value = (self.t._username, self.t._password)

    def test_connect_calls_sqlalchemy_engine_connect(self):
        self.t.engine = mock.Mock()
        self.t.connect()
        self.t.engine.connect.assert_called_once()

    @mock.patch('wrds.sql.sa')
    def test_connect_calls_get_user_credentials_on_exception(self, mock_sa):
        self.t.engine = mock.Mock()
        self.t.engine.connect.side_effect = Exception('Fake exception for testing')
        self.t.connect()
        self.t._Connection__get_user_credentials.assert_called_once()

    @mock.patch('wrds.sql.sa')
    def test_connect_calls_sqlalchemy_create_engine_on_exception(self, mock_sa):
        self.t.engine = mock.Mock()
        self.t.engine.connect.side_effect = Exception('Fake exception for testing')
        connstring = 'postgresql://{usr}:{pwd}@{host}:{port}/{dbname}'
        connstring = connstring.format(
            usr=self.t._username,
            pwd=self.t._password,
            host=self.t._hostname,
            port=self.t._port,
            dbname=self.t._dbname)
        self.t.connect()
        mock_sa.create_engine.assert_called_with(
            connstring,
            connect_args={'sslmode': 'require'})


class TestCreatePgpassFile(unittest.TestCase):
    def setUp(self):
        self.t = wrds.Connection(autoconnect=False)
        self.t._Connection__get_user_credentials = mock.Mock()
        self.t._Connection__get_user_credentials.return_value = ('faketestusername', 'faketestpassword')
        self.t._Connection__create_pgpass_file_win32 = mock.Mock()
        self.t._Connection__create_pgpass_file_unix = mock.Mock()

    def test_create_pgpass_calls_get_user_credentials_if_not_username(self):
        self.t._username = None
        self.t.create_pgpass_file()
        self.t._Connection__get_user_credentials.assert_called_once()

    def test_create_pgpass_calls_get_user_credentials_if_not_password(self):
        self.t._password = None
        self.t.create_pgpass_file()
        self.t._Connection__get_user_credentials.assert_called_once()

    @unittest.skipIf(sys.platform != 'win32', 'Windows-only test')
    def test_create_pgpass_calls_win32_version_if_windows(self):
        self.t.create_pgpass_file()
        self.t._Connection__create_pgpass_file_win32.assert_called_once()

    @unittest.skipIf(sys.platform == 'win32', 'Unix-only test')
    def test_create_pgpass_calls_unix_version_if_unix(self):
        self.t.create_pgpass_file()
        self.t._Connection__create_pgpass_file_unix.assert_called_once()


if (__name__ == '__main__'):
    unittest.main()
