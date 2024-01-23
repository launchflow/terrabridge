terrabridge
===========

|license| |CI| |Python version| |codecov|

.. |license| image:: https://img.shields.io/pypi/l/terrabridge.svg
    :target: https://pypi.python.org/pypi/terrabridge
.. |CI| image:: https://github.com/launchflow/terrabridge/actions/workflows/python_ci.yaml/badge.svg
    :target: https://github.com/launchflow/terrabridge/actions/workflows/python_ci.yaml
.. |Python version| image:: https://badge.fury.io/py/terrabridge.svg
   :target: https://pypi.org/project/terrabridge
.. |codecov| image:: https://codecov.io/gh/launchflow/terrabridge/graph/badge.svg?token=slFk4lUP2h
   :target: https://codecov.io/gh/launchflow/terrabridge


Terrabridge bridges the gap between Terraform and applicatoin code. With
Terrabridge you simply provide your terraform state file to the library
and all information will be loaded allowing you to easily access your
resources. This allows you to truly keep your infrastructure
configuration in one place.

Once your terraform and application code are in sync Terrabridge makes
it dead simple to connect to your resource by providing easy ready to
use clients for your resources such as SQLAlchemy for relational
databases, or reading secret values from secret storage.

.. code:: python

   from terrabridge.gcp import SecretManagerSecret

   sec = SecretManagerSecret("secret", state_file="terraform.tfstate")
   print(sec.version().decode("utf-8"))

Installation
------------

.. code:: bash

   pip install terrabridge

To use the GCP clients you will need to install the GCP extras:

.. code:: bash

   pip install terrabridge[gcp]

To use the AWS clients you will need to install the AWS extras:

.. code:: bash

   pip install terrabridge[aws]

Usage
-----

Basic Usage
~~~~~~~~~~~

Terrabridge can be used by providing your state file to the library. The
state file can be local, stored in an S3 bucket, or in a GCS bucket.
Terrabridge will then parse the state file into a python object that can
be consumed by your application code.

For example if you had the below terraform code that creates and manages
a GCS bucket you can easily access the bucket from your application code
using the ``GCSBucket`` class. All terrabridge objects take in a state
file and the name of the resource you assigned in terraform. All
attributes that are available in terraform are now available on your
terrabridge object.

.. code:: python

   from terrabridge.gcp import GCSBucket

   bucket = GCSBucket("bucket", state_file="terraform.tfstate")
   # Fetches the remote bucket.
   print(bucket.url)
   print(bucket.id)
   print(bucket.name)
   bucket = bucket.bucket()
   print(bucket.get_iam_policy().bindings)

.. code:: hcl

   resource "google_storage_bucket" "bucket" {
       name = var.bucket_name
       location = "US"
   }

Global State File
~~~~~~~~~~~~~~~~~

If all of your terrabridge objects use the same state file you can set a
global state file, and avoid passing it to each object:

.. code:: python

   import terrabridge
   from terrabridge.gcp import GCSBucket

   terrabridge.state_file="terraform.tfstate"

   bucket = GCSBucket("bucket")

Remote State File
~~~~~~~~~~~~~~~~~

If your state file is stored in an S3 bucket or GCS bucket you can pass
the bucket name and key to the ``state_file`` argument. Terrabridge will
then download the state file and parse it.

.. code:: python


   from terrabridge.gcp import GCSBucket
   from terrabridge.aws import S3Bucket

   gcs_bucket = GCSBucket("bucket", state_file="gs://my-bucket/terraform.tfstate")
   s3_bucket = S3Bucket("bucket", state_file="s3://my-bucket/terraform.tfstate")

Examples
--------

S3 Bucket
~~~~~~~~~

Easily connect and read data from a S3 bucket, that is defined in
terraform.

TODO

GCS Bucket
~~~~~~~~~~

Easily connect and read data from a GCS bucket, that is defined in
terraform.

**Python:**

.. code:: python

   from terrabridge.gcp import GCSBucket

   bucket = GCSBucket("bucket", state_file="terraform.tfstate")
   bucket = bucket.bucket()
   print(bucket.get_iam_policy().bindings)

**Terraform:**

.. code:: hcl

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

Cloud SQL Postgres Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use SQLAlchemy to connect to a managed Cloud SQL Postgres database with
one function call.

**Python:**

.. code:: python

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

**Terraform:**

.. code:: hcl

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

Supported Providers and Languages
---------------------------------

Python in the first language we support however we plan to support more
languages in the future. We are always happy to accept contributions for
new languages and providers.

========= ========== ========== ======== ==============
\         **python** **golang** **java** **typescript**
========= ========== ========== ======== ==============
**gcp**   ✅         ❌         ❌       ❌
**aws**   🚧         ❌         ❌       ❌
**azure** ❌         ❌         ❌       ❌
========= ========== ========== ======== ==============

GCP Supported Resources
~~~~~~~~~~~~~~~~~~~~~~~

TODO: add links to docs

-  BigQuery Dataset
-  BigQuery Instance
-  BigTable Instance
-  BigTable Table
-  Cloud SQL Database Instance
-  Cloud SQL Database
-  Cloud SQL User
-  Cloud Tasks Queue
-  GCS Bucket
-  Pub/Sub Lite Topic
-  Pub/Sub Lite Subscription
-  Pub/Sub Topic
-  Pub/Sub Subscription
-  Secret Manager Secret

AWS Supported Resources
~~~~~~~~~~~~~~~~~~~~~~~

 TODO
