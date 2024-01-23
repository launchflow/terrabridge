from typing import Optional

from terrabridge.gcp.base import GCPResource


class BigQueryDataset(GCPResource):
    """Represents a BigQuery Dataset

    Parsed from the terraform resource: ``google_bigquery_dataset``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import BigQueryDataset

        dataset = BigQueryDataset("dataset", state_file="gs://my-bucket/terraform.tfstate")
        print(dataset.id)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
    """

    _terraform_type = "google_bigquery_dataset"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)


class BigQueryTable(GCPResource):
    """Represents a BigQuery Table

    Parsed from the terraform resource: ``google_bigquery_table``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table>`_.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import BigQueryTable

        table = BigQueryTable("table", state_file="gs://my-bucket/terraform.tfstate")
        print(table.id)
        print(table.dataset.id)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        dataset (BigQueryDataset): The dataset the table belongs to. Will only be
            populated if the dataset also exists in the state file.
    """

    _terraform_type = "google_bigquery_table"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.dataset: Optional[BigQueryDataset] = None
        for dependency in self._dependencies:
            if dependency.startswith(BigQueryDataset._terraform_type):
                self.dataset = BigQueryDataset(
                    dependency.split(".")[1], state_file=state_file
                )
