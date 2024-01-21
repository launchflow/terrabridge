from typing import Optional
import sqlalchemy
from google.cloud.sql.connector import IPTypes

class CloudSQLInstance:
    connection_name: str
    database_version: str
    name: str

class CloudSQLUser:
    name: str
    password: str
    cloud_sql_instance: Optional[CloudSQLInstance]

class CloudSQLDatabase:
    name: str
    cloud_sql_instance: Optional[CloudSQLInstance]

    def sqlalchemy_engine(
        self, user: CloudSQLUser, ip_type: IPTypes = IPTypes.PUBLIC, **engine_params
    ) -> sqlalchemy.engine.base.Engine: ...
    async def async_sqlalchemy_engine(
        self, user: CloudSQLUser, ip_type: IPTypes = IPTypes.PUBLIC, **engine_params
    ) -> sqlalchemy.ext.asyncio.AsyncEngine: ...
