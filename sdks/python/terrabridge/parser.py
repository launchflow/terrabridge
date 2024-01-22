# Maps a terraform type to a resource type.
import json
from typing import Any, Dict

import gcsfs
import s3fs
from fsspec.implementations.local import LocalFileSystem

# Maps a terraform state file to the resources contained in it.
tf_state_cache: Dict[str, Dict[str, Dict[str, Any]]] = {}


def get_resource(resource_name: str, tf_state_path: str):
    """Return the attributes of a resource."""
    if tf_state_path not in tf_state_cache:
        _parse_terraform_state(tf_state_path)
    try:
        return tf_state_cache[tf_state_path][resource_name]
    except KeyError:
        raise ValueError(
            f"Resource {resource_name} not found in {tf_state_path}. "
            f"Available resources: {list(tf_state_cache[tf_state_path].keys())}"
        )


def _parse_terraform_state(tf_state_path: str):
    """Parse a terraform state file and return a list of resources."""
    if tf_state_path.startswith("gs://"):
        fs = gcsfs.GCSFileSystem()
    elif tf_state_path.startswith("s3://"):
        fs = s3fs.S3FileSystem()
    else:
        fs = LocalFileSystem()
    with fs.open(tf_state_path) as f:
        tf_state = json.load(f)
    if tf_state_path not in tf_state_cache:
        tf_state_cache[tf_state_path] = {}
    for resource in tf_state["resources"]:
        tf_state_cache[tf_state_path][resource["name"]] = {
            "attributes": resource["instances"][0].get("attributes", {}),
            "dependencies": resource["instances"][0].get("dependencies", {}),
            "type": resource["type"],
        }
