import sys
from unittest import mock

import pytest


def test_create_pgpass_calls_get_user_credentials_if_not_username(mock_connection):
    """Test create_pgpass_file calls get_user_credentials when username is None."""
    mock_connection._username = None
    mock_connection._Connection__create_pgpass_file_win32 = mock.Mock()
    mock_connection._Connection__create_pgpass_file_unix = mock.Mock()
    mock_connection.create_pgpass_file()
    mock_connection._Connection__get_user_credentials.assert_called_once()


def test_create_pgpass_calls_get_user_credentials_if_not_password(mock_connection):
    """Test create_pgpass_file calls get_user_credentials when password is None."""
    mock_connection._password = None
    mock_connection._Connection__create_pgpass_file_win32 = mock.Mock()
    mock_connection._Connection__create_pgpass_file_unix = mock.Mock()
    mock_connection.create_pgpass_file()
    mock_connection._Connection__get_user_credentials.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
def test_create_pgpass_calls_win32_version_if_windows(mock_connection):
    """Test create_pgpass_file calls win32 version on Windows."""
    mock_connection._Connection__create_pgpass_file_win32 = mock.Mock()
    mock_connection._Connection__create_pgpass_file_unix = mock.Mock()
    mock_connection.create_pgpass_file()
    mock_connection._Connection__create_pgpass_file_win32.assert_called_once()


@pytest.mark.skipif(sys.platform == "win32", reason="Unix-only test")
def test_create_pgpass_calls_unix_version_if_unix(mock_connection):
    """Test create_pgpass_file calls unix version on Unix."""
    mock_connection._Connection__create_pgpass_file_win32 = mock.Mock()
    mock_connection._Connection__create_pgpass_file_unix = mock.Mock()
    mock_connection.create_pgpass_file()
    mock_connection._Connection__create_pgpass_file_unix.assert_called_once()
