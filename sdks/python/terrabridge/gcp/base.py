from terrabridge.base import Resource


class GCPResource(Resource):
    """Base class for all GCP resources"""

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.project: str = self._attributes["project"]
        self.id: str = self._attributes["id"]
