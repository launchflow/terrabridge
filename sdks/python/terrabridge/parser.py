import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import gcsfs
import s3fs
from fsspec.implementations.local import LocalFileSystem

import terrabridge

# Maps a terraform state file to the resources contained in it.
tf_state_cache: Dict[str, Dict[str, Dict[str, Any]]] = {}


@dataclass(frozen=True)
class _ResourceKey:
    resource_name: str
    module_name: Optional[str]

    def __repr__(self) -> str:
        if self.module_name is None:
            return self.resource_name
        return f"{self.resource_name} in {self.module_name}"


def get_resource(resource_name: str, module_name: Optional[str], tf_state_path: str):
    """Return the attributes of a resource."""
    if tf_state_path not in tf_state_cache:
        _parse_terraform_state(tf_state_path)
    try:
        return tf_state_cache[tf_state_path][_ResourceKey(resource_name, module_name)]
    except KeyError:
        raise ValueError(
            f"Resource {resource_name} not found in {tf_state_path}. "
            f"Available resources: {list(tf_state_cache[tf_state_path].keys())}"
        )


def _parse_terraform_state(tf_state_path: str):
    """Parse a terraform state file and return a list of resources."""
    if tf_state_path.startswith("gs://"):
        token = None
        if terrabridge._anon_state_file_creds:
            token = "anon"
        fs = gcsfs.GCSFileSystem(token=token)
    elif tf_state_path.startswith("s3://"):
        fs = s3fs.S3FileSystem(anon=terrabridge._anon_state_file_creds)
    else:
        fs = LocalFileSystem()
    with fs.open(tf_state_path) as f:
        tf_state = json.load(f)
    if tf_state_path not in tf_state_cache:
        tf_state_cache[tf_state_path] = {}
    for resource in tf_state["resources"]:
        tf_state_cache[tf_state_path][
            _ResourceKey(resource["name"], resource.get("module"))
        ] = {
            "attributes": resource["instances"][0].get("attributes", {}),
            "dependencies": resource["instances"][0].get("dependencies", {}),
            "type": resource["type"],
        }
