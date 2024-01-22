# terrabridge

![CI](https://github.com/launchflow/terrabridge/actions/workflows/python_ci.yaml/badge.svg)
[![Python version](https://badge.fury.io/py/terrabridge.svg)](https://pypi.org/project/terrabridge)
[![codecov](https://codecov.io/gh/launchflow/terrabridge/graph/badge.svg?token=slFk4lUP2h)](https://codecov.io/gh/launchflow/terrabridge)

Terrabridge bridges the gap between Terraform and applicatoin code. With Terrabridge you simply provide your terraform state file to the library and all information will be loaded allowing you to easily access your resources. This allows you to truly keep your infrastructure configuration in one place.

Once your terraform and application code are in sync Terrabridge makes it dead simple to connect to your resource by providing easy ready to use clients for your resources such as SQLAlchemy for relational databases, or reading secret values from secret storage.

```python
from terrabridge.gcp import SecretManagerSecret

sec = SecretManagerSecret("secret", state_file="terraform.tfstate")
print(sec.version().decode("utf-8"))

```

## Installation

```bash
pip install terrabridge
```

## Examples

### S3 Bucket

Easy connect and read data from a S3 bucket, that is defined in terraform.

TODO

### GCS Bucket

Easy connect and read data from a GCS bucket, that is defined in terraform.

**Terraform:**
```hcl
variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

variable "bucket_name" {
    type = string
    description = "Name of the bucket."
}


provider "google" {
    project = var.gcp_project_id
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_storage_bucket" "bucket" {
    name = var.bucket_name
    location = "US"
}
```

**Python:**

```python
from terrabridge.gcp import GCSBucket

bucket = GCSBucket("bucket", state_file="terraform.tfstate")
bucket = bucket.bucket()
print(bucket.get_iam_policy().bindings)
```

### Cloud SQL Postgres Database

Use SQLAlchemy to connect to a Cloud SQL Postgres database with one function call.

**Terraform:**

```hcl
variable "gcp_project_id" {
    type = string
    description = "The GCP project to deploy resources into."
}

provider "google" {
    project = var.gcp_project_id
    region  = "us-central1"
    zone    = "us-central1-a"
}

resource "google_sql_database_instance" "postgres_sql_instance" {
    name = "terrabridge-testing-instance-mysql"
    project = var.gcp_project_id
    database_version = "POSTGRES_15"
    region = "us-central1"
    settings {
        tier = "db-custom-1-3840"
    }
}

resource "google_sql_database" "postgres_database" {
    name = "terrabridge-testing-database"
    project = var.gcp_project_id
    instance = google_sql_database_instance.postgres_sql_instance.name
}

resource "google_sql_user" "postgres_user" {
    name = "terrabridge-testing-user"
    project = var.gcp_project_id
    instance = google_sql_database_instance.postgres_sql_instance.name
    password = "terrabridge-testing-password"
}
```

**Python:**

```python
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


db = CloudSQLDatabase("postgres_database", state_file="terraform.tfstate")
user = CloudSQLUser("postgres_user", state_file="terraform.tfstate")
engine = db.sqlalchemy_engine(user)

Base.metadata.create_all(engine)

conn = engine.connect()
print(conn.execute(select(StorageUser)).all())
```

## Supported Providers and Languages

Python in the first language we support however we plan to support more languages in the future. We are always happy to accept contributions for new languages and providers.

|           | **python** | **golang** | **java** | **typescript** |
|-----------|------------|------------|----------|----------------|
| **gcp**   | ✅          | ❌          | ❌        | ❌              |
| **aws**   | 🚧          | ❌          | ❌        | ❌              |
| **azure** | ❌          | ❌          | ❌        | ❌              |
