from typing import Optional

from terrabridge.gcp.base import GCPResource
from terrabridge.utils import parse_dependency

try:
    from google.cloud.sql.connector import Connector, IPTypes, create_async_connector
except ImportError:
    Connector = None
    IPTypes = None
    create_async_connector = None
try:
    import asyncpg
except ImportError:
    asyncpg = None
try:
    import pg8000
except ImportError:
    pg8000 = None
try:
    import pymysql
except ImportError:
    pymysql = None
try:
    import pytds
except ImportError:
    pytds = None
try:
    from sqlalchemy import Engine, create_engine
    from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
except ImportError:
    create_engine = None
    Engine = None
    create_async_engine = None
    AsyncEngine = None


class CloudSQLInstance(GCPResource):
    """Represents a CloudSQL Instance

    Parsed from the terraform resource: ``google_sql_database_instance``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import CloudSQLInstance

        sql_instance = CloudSQLInstance("instance", state_file="gs://my-bucket/terraform.tfstate")
        print(sql_instance.connection_name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        connection_name (str): The name of the instance.
        database_version (str): The database version.
        name (str): The name of the instance.
    """

    _terraform_type = "google_sql_database_instance"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.connection_name: str = self._attributes["connection_name"]
        self.database_version: str = self._attributes["database_version"]
        self.name: str = self._attributes["name"]


class CloudSQLUser(GCPResource):
    """Represents a CloudSQL User

    Parsed from the terraform resource: ``google_sql_user``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_user>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import CloudSQLUser

        sql_user = CloudSQLUser("user", state_file="gs://my-bucket/terraform.tfstate")
        print(sql_user.name)
        print(sql_user.password)
        print(sql_user.cloud_sql_instance.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the user.
        password (str): The password of the user.
        cloud_sql_instance (str): The instance the user belongs to. Will only be populated
            if the instance also exists in the state file.
    """

    _terraform_type = "google_sql_user"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name = self._attributes["name"]
        self.password = self._attributes["password"]
        self.cloud_sql_instance: Optional[CloudSQLInstance] = None
        for dependency in self._dependencies:
            dependency = parse_dependency(dependency)
            if dependency.resource_type == CloudSQLInstance._terraform_type:
                self.cloud_sql_instance = CloudSQLInstance(
                    resource_name=dependency.resource_name,
                    module_name=dependency.module,
                    state_file=state_file,
                )


class CloudSQLDatabase(GCPResource):
    """Represents a CloudSQL Database

    Parsed from the terraform resource: ``google_sql_database``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import CloudSQLDatabase

        database = CloudSQLDatabase("db", state_file="gs://my-bucket/terraform.tfstate")
        print(database.name)
        print(database.cloud_sql_instance.name)

        user = CloudSQLUser("user", state_file="gs://my-bucket/terraform.tfstate")
        engine = database.sqlalchemy_engine(user)
        async_engine = await database.async_sqlalchemy_engine(user)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the database.
        cloud_sql_instance (str): The instance the user belongs to. Will only be populated
            if the instance also exists in the state file.
    """

    _terraform_type = "google_sql_database"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name: str = self._attributes["name"]
        self.cloud_sql_instance: Optional[CloudSQLInstance] = None
        for dependency in self._dependencies:
            dependency = parse_dependency(dependency)
            if dependency.resource_type == CloudSQLInstance._terraform_type:
                self.cloud_sql_instance = CloudSQLInstance(
                    resource_name=dependency.resource_name,
                    module_name=dependency.module,
                    state_file=state_file,
                )

    def sqlalchemy_engine(
        self, user: CloudSQLUser, ip_type: IPTypes = IPTypes.PUBLIC, **engine_params
    ) -> Engine:
        """Returns a SQLAlchemy engine for the database.

        Requires ``terrabridge[gcp]`` and ``sqlalchemy`` to be installed, and whatever
        driver is needed for the database version.

        * ``POSTGRES``: ``pip install pg8000``
        * ``SQLSERVER``: ``pip install pytds``
        * ``MYSQL``: ``pip install pymysql``

        Parameters:
            user: The user to connect to the database with.
            ip_type: The type of IP address to connect with and.
            engine_params: Additional parameters to pass to the SQLAlchemy engine.

        Returns:
            A SQLAlchemy engine.
        """
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install terrabridge[gcp]`."
            )
        if Connector is None:
            raise ImportError(
                "google-cloud-sql-connector is not installed. "
                "Please install it with `pip install terrabridge[gcp]`."
            )
        if self.cloud_sql_instance.database_version.startswith("MYSQL"):
            if pymysql is None:
                raise ImportError(
                    "pymsql is not installed. Please install it "
                    "with `pip install pymysql`."
                )
            driver = "pymysql"
            url = "mysql+pymysql://"
        elif self.cloud_sql_instance.database_version.startswith("POSTGRES"):
            if pg8000 is None:
                raise ImportError(
                    "pg8000 is not installed. Please install it "
                    "with `pip install pg8000`."
                )
            driver = "pg8000"
            url = "postgresql+pg8000://"
        elif self.cloud_sql_instance.database_version.startswith("SQLSERVER"):
            if pytds is None:
                raise ImportError(
                    "pytds is not installed. Please install it "
                    "with `pip install pytds`."
                )
            driver = "pytds"
            url = "mssql+pytds://"
        else:
            raise NotImplementedError(
                f"Unknown database version: {self.cloud_sql_instance.database_version}"
            )
        connector = Connector(ip_type)

        def getconn() -> pytds.Connection:
            conn = connector.connect(
                self.cloud_sql_instance.connection_name,
                driver,
                user=user.name,
                password=user.password,
                db=self.name,
            )
            return conn

        return create_engine(url, creator=getconn, *engine_params)

    async def async_sqlalchemy_engine(
        self, user: CloudSQLUser, ip_type: IPTypes = IPTypes.PUBLIC, **engine_params
    ) -> AsyncEngine:
        """Returns a SQLAlchemy engine for the database.

        Requires ``terrabridge[gcp]`` and ``sqlalchemy[asyncio]`` to be installed.

        Parameters:
            user: The user to connect to the database with.
            ip_type: The type of IP address to connect with and.
            engine_params: Additional parameters to pass to the SQLAlchemy engine.

        Returns:
            A SQLAlchemy engine.
        """
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )
        if Connector is None:
            raise ImportError(
                "google-cloud-sql-connector is not installed. "
                "Please install it with `pip install terrabridge[gcp]`."
            )
        connector = await create_async_connector()

        if self.cloud_sql_instance.database_version.startswith("MYSQL"):
            raise NotImplementedError("async engine with mysql is not implemented")
        elif self.cloud_sql_instance.database_version.startswith("POSTGRES"):
            if asyncpg is None:
                raise ImportError(
                    "asyncpg is not installed. Please install "
                    "it with `pip install asyncpg`."
                )
            driver = "asyncpg"
            url = "postgresql+asyncpg://"
        elif self.cloud_sql_instance.database_version.startswith("SQLSERVER"):
            raise NotImplementedError("async engine with sqlserver is not implemented")

        # initialize Connector object for connections to Cloud SQL
        async def getconn() -> asyncpg.Connection:
            conn: asyncpg.Connection = await connector.connect_async(
                instance_connection_string=self.cloud_sql_instance.connection_name,
                driver=driver,
                user=user.name,
                password=user.password,
                db=self.name,
                ip_type=ip_type,
            )
            return conn

        return create_async_engine(url, async_creator=getconn, **engine_params)
