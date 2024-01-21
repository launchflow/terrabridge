from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import storage
except ImportError:
    storage = None


class GCSBucket(GCPResource):
    """Represents a GCS Bucket

    Parsed from the terraform resource: `google_storage_bucket`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket).

    Example usage:

    ```python
    from terrabridge.gcp import GCSBucket

    bucket = GCSBucket("queue", state_file="gs://my-bucket/terraform.tfstate")
    print(bucket.name)

    bucket.bucket().upload_from_filename("local_file.txt")
    ```
    """

    _terraform_type = "google_storage_bucket"
    _client = None

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.url: str = self._attributes["url"]
        self.name: str = self._attributes["name"]

    def bucket(self) -> storage.Bucket:
        """Fetches the remote storage bucket.

        Requires terrabridge[gcp] to be installed.
        """
        if storage is None:
            raise ImportError(
                "google-cloud-storage is not installed. Please install it with `pip install terrabridge[gcp]`."
            )
        if self._client is None:
            self._client = storage.Client()
        return self._client.get_bucket(self.name)
