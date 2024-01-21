from terrabridge.parser import get_resource


class Resource:
    _attributes = {}
    _terraform_type = None

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        self.resource_name = resource_name
        resource = get_resource(resource_name, state_file)
        if resource["type"] != self._terraform_type:
            raise ValueError(
                f"Resource {resource_name} is of type {resource['type']}, "
                f"but expected {self._terraform_type}."
            )
        self._attributes = resource["attributes"]
        self._dependencies = resource["dependencies"]

    def __getattr__(self, name):
        try:
            super().__getattr__(name)
        except AttributeError:
            try:
                return self._attributes[name]
            except KeyError:
                raise AttributeError(
                    f"Resource {self.resource_name} does not have attribute {name}"
                )

    def __str__(self) -> str:
        return str(self._attributes)
