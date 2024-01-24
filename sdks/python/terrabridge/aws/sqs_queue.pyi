from typing import Any, Dict, Optional

from mypy_boto3_sqs.service_resource import Queue

class SQSQueue:
    arn: str
    id: str
    url: str
    region: str

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None,
    ) -> None: ...
    def send_message(
        self,
        message_body: str,
        delay_seconds: Optional[int],
        message_attributes: Dict[str, Any] = {},
        message_system_attributes: Dict[str, Any] = {},
        deduplication_id: Optional[str] = None,
        message_group_id: Optional[str] = None,
    ) -> Dict[str, Any]: ...
    def queue(self) -> Queue: ...
