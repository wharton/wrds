import urllib.parse
from unittest import mock


def test_connect_calls_sqlalchemy_engine_connect(mock_connection):
    """Test connect calls sqlalchemy engine connect."""
    with mock.patch("wrds.sql.sa") as mock_sa:
        mock_engine = mock.Mock()
        mock_sa.create_engine.return_value = mock_engine
        mock_connection.connect()
        mock_engine.connect.assert_called_once()


def test_connect_calls_get_user_credentials_on_exception(mock_connection):
    """Test connect calls get_user_credentials when engine.connect raises exception."""
    with mock.patch("wrds.sql.sa") as mock_sa:
        with mock.patch("builtins.input", return_value="n"):
            # Make create_engine fail twice, then succeed on third attempt
            mock_sa.create_engine.side_effect = [
                Exception("Fake exception for testing"),
                Exception("Fake exception for testing"),
                mock.Mock(),
            ]
            mock_connection.connect()
            mock_connection._Connection__get_user_credentials.assert_called_once()


def test_connect_calls_sqlalchemy_create_engine_on_exception(mock_connection):
    """Test connect calls sqlalchemy create_engine when engine.connect raises exception."""
    import wrds

    with mock.patch("wrds.sql.sa") as mock_sa:
        with mock.patch("builtins.input", return_value="n"):
            # Make create_engine fail twice, then succeed on third attempt
            mock_engine = mock.Mock()
            mock_sa.create_engine.side_effect = [
                Exception("Fake exception for testing"),
                Exception("Fake exception for testing"),
                mock_engine,
            ]
            # After failures, hostname changes to default WRDS host
            connstring = "postgresql://{usr}:{pwd}@{host}:{port}/{dbname}"
            connstring = connstring.format(
                usr=mock_connection._username,
                pwd=urllib.parse.quote_plus(mock_connection._password),
                host=wrds.sql.WRDS_POSTGRES_HOST,  # Uses default host after retry
                port=mock_connection._port,
                dbname=mock_connection._dbname,
            )
            mock_connection.connect()
            # Check that the last call (third attempt) uses the correct connection string
            last_call_args = mock_sa.create_engine.call_args_list[-1]
            assert last_call_args[0][0] == connstring
            assert last_call_args[1]["isolation_level"] == "AUTOCOMMIT"
            assert last_call_args[1]["connect_args"]["sslmode"] == "require"
