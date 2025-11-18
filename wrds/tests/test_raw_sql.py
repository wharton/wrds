from unittest import mock


def test_rawsql_takes_unparameterized_sql(mock_connection):
    """Test raw_sql handles unparameterized SQL queries."""
    with mock.patch("wrds.sql.sa"):
        with mock.patch("wrds.sql.pd") as mock_pd:
            mock_connection.connection = mock.Mock()
            mock_connection.engine = mock.Mock()
            sql = "SELECT * FROM information_schema.tables LIMIT 1"
            mock_connection.raw_sql(sql)
            mock_pd.read_sql_query.assert_called_once_with(
                sql,
                mock_connection.connection,
                coerce_float=True,
                parse_dates=None,
                index_col=None,
                chunksize=500000,
                params=None,
                dtype=None,
                dtype_backend="numpy_nullable",
            )


def test_rawsql_takes_parameterized_sql(mock_connection):
    """Test raw_sql handles parameterized SQL queries."""
    with mock.patch("wrds.sql.sa"):
        with mock.patch("wrds.sql.pd") as mock_pd:
            mock_connection.connection = mock.Mock()
            mock_connection.engine = mock.Mock()
            sql = (
                "SELECT * FROM information_schema.tables "
                "WHERE table_name = %(tablename)s LIMIT 1"
            )
            tablename = "pg_stat_activity"
            mock_connection.raw_sql(sql, params=tablename)
            mock_pd.read_sql_query.assert_called_once_with(
                sql,
                mock_connection.connection,
                coerce_float=True,
                parse_dates=None,
                index_col=None,
                chunksize=500000,
                params=tablename,
                dtype=None,
                dtype_backend="numpy_nullable",
            )
