import datetime
import uuid

from sqlalchemy import Column, DateTime, Integer, select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from terrabridge.gcp import CloudSQLDatabase, CloudSQLUser


class Base(AsyncAttrs, DeclarativeBase):
    pass


class StorageUser(Base):
    __tablename__ = "users"

    # Autopoluated fields
    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


db = CloudSQLDatabase("sql_server_database", state_file="terraform.tfstate")
user = CloudSQLUser("sql_server_user", state_file="terraform.tfstate")
engine = db.sqlalchemy_engine(user)

Base.metadata.create_all(engine)

conn = engine.connect()
print(conn.execute(select(StorageUser)).all())
