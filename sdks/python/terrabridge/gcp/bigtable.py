from typing import Optional
from terrabridge.gcp.base import GCPResource


class BigTableInstance(GCPResource):
    """Represents a BigTable Instance

    Parsed from the terraform resource: `google_bigtable_instance`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_instance).

    Example usage:

    ```python
    from terrabridge.gcp import BigTableInstance

    bt_instance = BigTableInstance("instance", state_file="gs://my-bucket/terraform.tfstate")
    print(instance.name)
    ```
    """

    _terraform_type = "google_bigtable_instance"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name: str = self._attributes["name"]


class BigTableTable(GCPResource):
    """Represents a BigTable Table

    Parsed from the terraform resource: `google_bigtable_table`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_table).

    Example usage:

    ```python
    from terrabridge.gcp import BigTableTable

    table = BigTableTable("table", state_file="gs://my-bucket/terraform.tfstate")
    print(table.name)
    print(table.instance.name)
    ```
    """

    _terraform_type = "google_bigtable_table"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.instance: Optional[BigTableInstance] = None
        self.name: str = self._attributes["name"]
        for dependency in self._dependencies:
            if dependency.startswith(BigTableInstance._terraform_type):
                self.instance = BigTableInstance(
                    dependency.split(".")[1], state_file=state_file
                )
