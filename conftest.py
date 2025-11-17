from unittest import mock

import pytest


@pytest.fixture
def mock_connection():
    """Create a mock wrds.Connection instance for testing."""
    import wrds

    conn = wrds.Connection(autoconnect=False)
    conn._hostname = "wrds.test.private"
    conn._port = 12345
    conn._username = "faketestusername"
    conn._password = "faketestuserpass"
    conn._dbname = "testdbname"
    conn._Connection__get_user_credentials = mock.Mock()
    conn._Connection__get_user_credentials.return_value = (
        conn._username,
        conn._password,
    )
    return conn
