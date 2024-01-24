from typing import Any, Dict, Optional

from terrabridge.aws.base import AWSResource

try:
    import boto3
    from mypy_boto3_sqs.service_resource import Queue
except ImportError:
    queue = object
    boto3 = None


class SQSQueue(AWSResource):
    """Represents a SQS Queue

    Parsed from the terraform resource: ``aws_sqs_queue``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sqs_queue>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.aws import SQSQueue

        # Load a SQS queue from terraform state
        queue = SQSQueue("queue", state_file="terraform.tfstate")
        print(queue.url)

        # Fetch the remote queue from boto3 and print number of outstanding messages
        boto_queue = queue.queue()
        print(boto_queue.attributes["ApproximateNumberOfMessages"])

        # Send a message to the queue
        queue.send_message("test", delay_seconds=2)

    Attributes:
        arn (str): The ARN assigned to the resource.
        id (str): The id of the resource.
        url (str): The url of the queue (this is the same as ID).
        region (str): The region the resource belongs to.
    """

    _terraform_type = "aws_sqs_queue"
    _client = None
    _queue = None

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.url: str = self._attributes["url"]
        self.region = self.arn.split(":")[3]

    def send_message(
        self,
        message_body: str,
        delay_seconds: Optional[int] = None,
        message_attributes: Optional[Dict[str, Any]] = None,
        message_system_attributes: Optional[Dict[str, Any]] = None,
        deduplication_id: str = None,
        message_group_id: str = None,
    ) -> Dict[str, Any]:
        """
        Sends a message to the queue.

        Args:
            message_body: The message to send.
            delay_seconds: The number of seconds to delay the message before
                sending it to subscribers.
            message_attributes: The attributes of the message.
            message_system_attributes: The system attributes of the message.
            deduplication_id: The deduplication ID of the message.
            message_group_id: The message group ID of the message.

        Returns:
            Dict[str, Any]: The response from boto3.
        """
        if boto3 is None:
            raise ImportError(
                "boto3 is not installed. "
                "Please install it with `pip install terrabridge[aws]`."
            )
        if self._client is None:
            self._client = boto3.resource("sqs", region_name=self.region)
        if self._queue is None:
            self._queue = self._client.Queue(self.url)

        request = {
            "QueueUrl": self.url,
            "MessageBody": message_body,
        }
        if delay_seconds is not None:
            request["DelaySeconds"] = delay_seconds
        if message_attributes is not None:
            request["MessageAttributes"] = message_attributes
        if message_system_attributes is not None:
            request["MessageSystemAttributes"] = message_system_attributes
        if deduplication_id is not None:
            request["MessageDeduplicationId"] = deduplication_id
        if message_group_id is not None:
            request["MessageGroupId"] = message_group_id
        return self._queue.send_message(**request)

    def queue(self) -> Queue:
        """Fetches the queue using boto3

        Returns:
            Queue: The queue object from boto3
        """
        if boto3 is None:
            raise ImportError(
                "boto3 is not installed. "
                "Please install it with `pip install terrabridge[aws]`."
            )
        if self._client is None:
            self._client = boto3.resource("sqs", region_name=self.region)
        if self._queue is None:
            self._queue = self._client.Queue(self.url)

        return self._queue
