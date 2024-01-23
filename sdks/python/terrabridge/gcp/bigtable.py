from typing import Optional

from terrabridge.gcp.base import GCPResource


class BigTableInstance(GCPResource):
    """Represents a BigTable Instance

    Parsed from the terraform resource: ``google_bigtable_instance``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_instance>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import BigTableInstance

        bt_instance = BigTableInstance("instance", state_file="gs://my-bucket/terraform.tfstate")
        print(instance.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the instance.
    """

    _terraform_type = "google_bigtable_instance"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name: str = self._attributes["name"]


class BigTableTable(GCPResource):
    """Represents a BigTable Table

    Parsed from the terraform resource: ``google_bigtable_table``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigtable_table>_`.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import BigTableTable

        table = BigTableTable("table", state_file="gs://my-bucket/terraform.tfstate")
        print(table.name)
        print(table.instance.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the table.
        instance (BigTableInstance): The instance the table belongs to. Will only be
            populated if the instance also exists in the state file.
    """

    _terraform_type = "google_bigtable_table"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, state_file=state_file, module_name=module_name)
        self.instance: Optional[BigTableInstance] = None
        self.name: str = self._attributes["name"]
        for dependency in self._dependencies:
            if dependency.startswith(BigTableInstance._terraform_type):
                self.instance = BigTableInstance(
                    dependency.split(".")[1], state_file=state_file
                )
