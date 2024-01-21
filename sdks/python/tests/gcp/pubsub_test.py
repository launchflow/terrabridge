from terrabridge.gcp import PubSubSubscription, PubSubTopic


def test_pubsub_topic():
    topic = PubSubTopic(
        resource_name="topic", state_file="tests/data/terraform.tfstate"
    )

    assert topic.project == "terrabridge-testing"
    assert topic.name == "example-topic"
    assert topic.id == "projects/terrabridge-testing/topics/example-topic"


def test_pubsub_subscription():
    subscription = PubSubSubscription(
        resource_name="subscription", state_file="tests/data/terraform.tfstate"
    )

    assert subscription.project == "terrabridge-testing"
    assert subscription.name == "example-subscription"
    assert (
        subscription.id
        == "projects/terrabridge-testing/subscriptions/example-subscription"
    )
