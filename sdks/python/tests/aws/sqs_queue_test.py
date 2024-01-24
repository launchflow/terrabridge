from unittest.mock import MagicMock, patch

from terrabridge.aws import SQSQueue


def test_sqs_queue():
    queue = SQSQueue(
        resource_name="queue",
        state_file="tests/data/aws/terraform.tfstate",
    )

    assert queue.arn == "arn:aws:sqs:us-east-1:123456:terrabridge-testing-queue"
    assert (
        queue.id
        == "https://sqs.us-east-1.amazonaws.com/123456/terrabridge-testing-queue"
    )
    assert queue.region == "us-east-1"
    assert queue.resource_name == "queue"
    assert (
        queue.url
        == "https://sqs.us-east-1.amazonaws.com/123456/terrabridge-testing-queue"
    )

    with patch("boto3.resource") as mock:
        to_ret = MagicMock()
        mock.return_value.Queue.return_value = to_ret
        boto_queue = queue.queue()
        queue.send_message(
            "test",
            delay_seconds=2,
            message_attributes={"test": "test"},
            message_system_attributes={"test1": "test1"},
            deduplication_id="de",
            message_group_id="gr",
        )
        assert boto_queue == to_ret
        mock.assert_called_once()
        mock.return_value.Queue.assert_called_once_with(
            "https://sqs.us-east-1.amazonaws.com/123456/terrabridge-testing-queue"
        )
        boto_queue.send_message.assert_called_once_with(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/123456/terrabridge-testing-queue",
            MessageBody="test",
            DelaySeconds=2,
            MessageAttributes={"test": "test"},
            MessageSystemAttributes={"test1": "test1"},
            MessageDeduplicationId="de",
            MessageGroupId="gr",
        )
