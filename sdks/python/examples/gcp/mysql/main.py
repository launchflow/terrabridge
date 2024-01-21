import datetime
import uuid
from terrabridge.gcp import CloudSQLDatabase, CloudSQLUser

from sqlalchemy import Column, DateTime, Integer, select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class StorageUser(Base):
    __tablename__ = "users"

    # Autopoluated fields
    id = Column(Integer, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


db = CloudSQLDatabase("mysql_database", state_file="terraform.tfstate")
user = CloudSQLUser("mysql_user", state_file="terraform.tfstate")
engine = db.sqlalchemy_engine(user)

Base.metadata.create_all(engine)

conn = engine.connect()
print(conn.execute(select(StorageUser)).all())
