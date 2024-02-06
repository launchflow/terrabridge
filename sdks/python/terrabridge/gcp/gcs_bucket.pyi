from typing import Optional

from google.cloud import storage

class GCSBucket:
    _client: storage.Client
    url: str
    name: str
    project: str
    id: str

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None: ...
    def bucket(self) -> storage.Bucket: ...
