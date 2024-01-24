from unittest.mock import patch

from terrabridge.gcp import PubSubSubscription, PubSubTopic


def test_pubsub_topic():
    topic = PubSubTopic(
        resource_name="topic", state_file="tests/data/gcp/terraform.tfstate"
    )

    assert topic.project == "terrabridge-testing"
    assert topic.name == "example-topic"
    assert topic.id == "projects/terrabridge-testing/topics/example-topic"

    with patch("terrabridge.gcp.pubsub.pubsub_v1.PublisherClient") as mock:
        topic.publish(b"Hello, world!", ordering_key="123", foo="bar")

        mock.assert_called_once()
        mock.return_value.publish.assert_called_once_with(
            topic=topic.id, data=b"Hello, world!", ordering_key="123", foo="bar"
        )


def test_pubsub_subscription():
    subscription = PubSubSubscription(
        resource_name="subscription", state_file="tests/data/gcp/terraform.tfstate"
    )

    assert subscription.project == "terrabridge-testing"
    assert subscription.name == "example-subscription"
    assert (
        subscription.id
        == "projects/terrabridge-testing/subscriptions/example-subscription"
    )
