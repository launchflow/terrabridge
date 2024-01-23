from typing import Optional

from terrabridge.gcp.base import GCPResource


class CloudTasksQueue(GCPResource):
    """Represents a Cloud Tasks Queue

    Parsed from the terraform resource: ``google_cloud_tasks_queue``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_tasks_queue>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import CloudTasksQueue

        queue = CloudTasksQueue("queue", state_file="gs://my-bucket/terraform.tfstate")
        print(queue.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the cloud tasks queue.
    """

    _terraform_type = "google_cloud_tasks_queue"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name = self._attributes["name"]
