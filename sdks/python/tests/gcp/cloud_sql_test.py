from unittest.mock import ANY, patch

from terrabridge.gcp.cloud_sql import CloudSQLDatabase, CloudSQLInstance, CloudSQLUser

# TODO: add tests for sqlalchemy_engine and async_sqlalchemy_engine


def test_cloud_sql_instance():
    instance = CloudSQLInstance(
        resource_name="cloud_sql_instance", state_file="tests/data/terraform.tfstate"
    )

    assert instance.project == "terrabridge-testing"
    assert instance.resource_name == "cloud_sql_instance"
    assert instance.name == "terrabridge-testing-instance"
    assert (
        instance.connection_name
        == "terrabridge-testing:us-central1:terrabridge-testing-instance"
    )


def test_cloud_sql_database():
    database = CloudSQLDatabase(
        resource_name="database", state_file="tests/data/terraform.tfstate"
    )

    assert database.project == "terrabridge-testing"
    assert database.resource_name == "database"
    assert database.name == "terrabridge-testing-database"
    assert database.cloud_sql_instance.resource_name == "cloud_sql_instance"
    assert (
        database.cloud_sql_instance.connection_name
        == "terrabridge-testing:us-central1:terrabridge-testing-instance"
    )


def test_cloud_sql_user():
    user = CloudSQLUser(resource_name="user", state_file="tests/data/terraform.tfstate")

    assert user.project == "terrabridge-testing"
    assert user.resource_name == "user"
    assert user.cloud_sql_instance.resource_name == "cloud_sql_instance"
    assert (
        user.cloud_sql_instance.connection_name
        == "terrabridge-testing:us-central1:terrabridge-testing-instance"
    )
    assert user.name == "terrabridge-testing-user"
    assert user.password == "terrabridge-testing-password"


def test_cloud_sql_database_postgres_sqlalchemy():
    database = CloudSQLDatabase(
        resource_name="database", state_file="tests/data/terraform.tfstate"
    )
    user = CloudSQLUser(resource_name="user", state_file="tests/data/terraform.tfstate")

    with patch("terrabridge.gcp.cloud_sql.create_engine") as mock_create_engine:
        with patch("terrabridge.gcp.cloud_sql.Connector") as mock_connector:
            database.sqlalchemy_engine(user)
            mock_create_engine.assert_called_once_with(
                "postgresql+pg8000://", creator=ANY
            )

            creator = mock_create_engine.call_args.kwargs["creator"]
            creator()
            mock_connector.return_value.connect.assert_called_once_with(
                database.cloud_sql_instance.connection_name,
                "pg8000",
                user=user.name,
                password=user.password,
                db=database.name,
            )


def test_cloud_sql_database_mysql_sqlalchemy():
    database = CloudSQLDatabase(
        resource_name="mysql_database", state_file="tests/data/terraform.tfstate"
    )
    user = CloudSQLUser(
        resource_name="mysql_user1", state_file="tests/data/terraform.tfstate"
    )

    with patch("terrabridge.gcp.cloud_sql.create_engine") as mock_create_engine:
        with patch("terrabridge.gcp.cloud_sql.Connector") as mock_connector:
            database.sqlalchemy_engine(user)
            mock_create_engine.assert_called_once_with("mysql+pymysql://", creator=ANY)

            creator = mock_create_engine.call_args.kwargs["creator"]
            creator()
            mock_connector.return_value.connect.assert_called_once_with(
                database.cloud_sql_instance.connection_name,
                "pymysql",
                user=user.name,
                password=user.password,
                db=database.name,
            )


def test_cloud_sql_database_sqlserver_sqlalchemy():
    database = CloudSQLDatabase(
        resource_name="sql_server_database", state_file="tests/data/terraform.tfstate"
    )
    user = CloudSQLUser(
        resource_name="sql_server_user", state_file="tests/data/terraform.tfstate"
    )

    with patch("terrabridge.gcp.cloud_sql.create_engine") as mock_create_engine:
        with patch("terrabridge.gcp.cloud_sql.Connector") as mock_connector:
            database.sqlalchemy_engine(user)
            mock_create_engine.assert_called_once_with("mssql+pytds://", creator=ANY)

            creator = mock_create_engine.call_args.kwargs["creator"]
            creator()
            mock_connector.return_value.connect.assert_called_once_with(
                database.cloud_sql_instance.connection_name,
                "pytds",
                user=user.name,
                password=user.password,
                db=database.name,
            )
