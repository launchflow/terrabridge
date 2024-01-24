from typing import Optional

from terrabridge.aws.base import AWSResource

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


class DatabaseInstance(AWSResource):
    _terraform_type = "aws_db_instance"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.username: str = self._attributes["username"]
        self.password: str = self._attributes["password"]
        self.endpoint: str = self._attributes["endpoint"]
        self.engine: str = self._attributes["engine"]
        self.db_name: Optional[str] = self._attributes.get("db_name")

    def sqlachemy_engine(self):
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install terrabridge[gcp]`."
            )
        if self.engine == "postgres":
            if pg8000 is None:
                raise ImportError(
                    "pg8000 is not installed. Please install it "
                    "with `pip install pg8000`."
                )
            url = f"postgresql+pg8000://{self.username}:{self.password}@{self.endpoint}/{self.db_name}"
        else:
            raise ValueError(f"Unsupported engine: {self.engine}")
        return create_engine(url)
