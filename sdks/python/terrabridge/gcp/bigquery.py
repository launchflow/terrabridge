from typing import Optional
from terrabridge.gcp.base import GCPResource


class BigQueryDataset(GCPResource):
    """Represents a BigQuery Dataset

    Parsed from the terraform resource: `google_bigquery_dataset`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset).

    Example usage:

    ```python
    from terrabridge.gcp import BigQueryDataset

    dataset = BigQueryDataset("dataset", state_file="gs://my-bucket/terraform.tfstate")
    print(dataset.id)
    ```
    """

    _terraform_type = "google_bigquery_dataset"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)


class BigQueryTable(GCPResource):
    """Represents a BigQuery Table

    Parsed from the terraform resource: `google_bigquery_table`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table).

    Example usage:

    ```python
    from terrabridge.gcp import BigQueryTable

    table = BigQueryTable("table", state_file="gs://my-bucket/terraform.tfstate")
    print(table.id)
    print(table.dataset.id)
    ```
    """

    _terraform_type = "google_bigquery_table"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.dataset: Optional[BigQueryDataset] = None
        for dependency in self._dependencies:
            if dependency.startswith(BigQueryDataset._terraform_type):
                self.dataset = BigQueryDataset(
                    dependency.split(".")[1], state_file=state_file
                )
