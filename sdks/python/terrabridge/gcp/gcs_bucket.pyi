from google.cloud import storage

class GCSBucket:
    _client: storage.Client
    url: str
    name: str

    def __init__(self, resource_name: str, *, state_file: str) -> None: ...
    def bucket(self) -> storage.Bucket: ...
