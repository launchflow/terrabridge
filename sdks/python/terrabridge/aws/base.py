from typing import Optional

from terrabridge.base import Resource


class AWSResource(Resource):
    """Base class for all AWS resources.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Attributes:
        arn (str): The ARN assigned to the resource.
        id (str): The id of the resource.
    """

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.arn = self._attributes["arn"]
        self.id = self._attributes["id"]
