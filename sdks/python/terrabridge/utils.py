from dataclasses import dataclass
from typing import Optional


@dataclass
class Dependency:
    module: Optional[str]
    resource_type: str
    resource_name: str


def parse_dependency(dependency: str) -> Dependency:
    split = dependency.split(".")

    module = None
    if split[0] == "module":
        module = f"{split[0]}.{split[1]}"
        split = split[2:]
    resource_type = split[0]
    resource_name = split[1]
    return Dependency(module, resource_type, resource_name)
