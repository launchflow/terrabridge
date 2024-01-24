from typing import Optional

from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import storage
except ImportError:
    storage = None


class GCSBucket(GCPResource):
    """Represents a GCS Bucket

    Parsed from the terraform resource: ``google_storage_bucket``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import GCSBucket

        bucket = GCSBucket("bucket", state_file="gs://my-bucket/terraform.tfstate")
        print(bucket.name)

        bucket.bucket().upload_from_filename("local_file.txt")

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the bucket.
        url (str): The url of the bucket (e.g. gs://BUCKET_NAME).
    """

    _terraform_type = "google_storage_bucket"
    _client = None

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.url: str = self._attributes["url"]
        self.name: str = self._attributes["name"]

    def bucket(self) -> storage.Bucket:
        """Fetches the remote storage bucket.

        Requires ``terrabridge[gcp]`` to be installed.
        """
        if storage is None:
            raise ImportError(
                "google-cloud-storage is not installed. "
                "Please install it with `pip install terrabridge[gcp]`."
            )
        if self._client is None:
            self._client = storage.Client()
        return self._client.get_bucket(self.name)
