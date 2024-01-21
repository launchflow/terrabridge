from terrabridge.gcp import PubSubLiteSubscription, PubSubLiteTopic


def test_pubsub_lite_topic():
    topic = PubSubLiteTopic(
        resource_name="lite_topic", state_file="tests/data/terraform.tfstate"
    )

    assert topic.project == "terrabridge-testing"
    assert topic.name == "example-lite-topic"
    assert topic.id == (
        "projects/terrabridge-testing/locations"
        "/us-central1-a/topics/example-lite-topic"
    )


def test_pubsub_lite_subscription():
    subscription = PubSubLiteSubscription(
        resource_name="lite_sub", state_file="tests/data/terraform.tfstate"
    )

    assert subscription.project == "terrabridge-testing"
    assert subscription.name == "example-lite-subscription"
    assert subscription.id == (
        "projects/terrabridge-testing/locations/"
        "us-central1-a/subscriptions/example-lite-subscription"
    )
