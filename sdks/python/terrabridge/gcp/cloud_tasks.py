from terrabridge.gcp.base import GCPResource


class CloudTasksQueue(GCPResource):
    """Represents a Cloud Tasks Queue

    Parsed from the terraform resource: `google_cloud_tasks_queue`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/cloud_tasks_queue).

    Example usage:

    ```python
    from terrabridge.gcp import CloudTasksQueue

    queue = CloudTasksQueue("queue", state_file="gs://my-bucket/terraform.tfstate")
    print(queue.name)
    ```
    """

    _terraform_type = "google_cloud_tasks_queue"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name = self._attributes["name"]
