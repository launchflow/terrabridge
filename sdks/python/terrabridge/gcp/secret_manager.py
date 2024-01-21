from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import secretmanager
except ImportError:
    secretmanager = None


class SecretManagerSecret(GCPResource):
    """Represents a Secret Manager Secret

    Parsed from the terraform resource: `google_secret_manager_secret`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/secret_manager_secret).

    Example usage:

    ```python
    from terrabridge.gcp import SecretManagerSecret

    secret = SecretManagerSecret("subscription", state_file="gs://my-bucket/terraform.tfstate")
    print(secret.name)

    print(secret.version().decode("utf-8"))
    ```
    """

    _client = None
    _terraform_type = "google_secret_manager_secret"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name = self._attributes["name"]

    def version(self, version: str = "latest") -> bytes:
        """Fetches the secret version.

        Requires terrabridge[gcp] to be installed.
        """
        if secretmanager is None:
            raise ImportError(
                "google-cloud-secret-manager is not installed. Please install it with `pip install terrabridge[gcp]`."
            )
        if self._client is None:
            self._client = secretmanager.SecretManagerServiceClient()
        return self._client.access_secret_version(
            name=f"{self.name}/versions/{version}"
        ).payload.data
