from typing import Optional

from mypy_boto3_s3.service_resource import Bucket

class S3Bucket:
    bucket: str
    arn: str
    id: str
    region: str

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None: ...
    def fetch_bucket(self) -> Bucket: ...
