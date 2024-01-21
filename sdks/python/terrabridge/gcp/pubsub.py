from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import pubsub_v1
except ImportError:
    pubsub_v1 = None


class PubSubTopic(GCPResource):
    """Represents a PubSub Topic

    Parsed from the terraform resource: `google_pubsub_topic`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic).

    Example usage:

    ```python
    from terrabridge.gcp import PubSubTopic

    topic = PubSubTopic("topic", state_file="gs://my-bucket/terraform.tfstate")
    print(topic.name)

    topic.publish(b"Hello, world!")
    ```
    """

    _publisher = None
    _terraform_type = "google_pubsub_topic"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name = self._attributes["name"]

    def publish(self, message: bytes, ordering_key: str = "", **attributes):
        if pubsub_v1 is None:
            raise ImportError(
                "google-cloud-pubsub is not installed. Please install it with `pip install terrabridge[gcp]`."
            )
        if self._publisher is None:
            self._publisher = pubsub_v1.PublisherClient()
        return self._publisher.publish(
            topic=self.id, data=message, ordering_key=ordering_key, **attributes
        )


class PubSubSubscription(GCPResource):
    """Represents a PubSub Subscription

    Parsed from the terraform resource: `google_pubsub_subscription`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription).

    Example usage:

    ```python
    from terrabridge.gcp import PubSubSubscription

    subscription = PubSubSubscription("subscription", state_file="gs://my-bucket/terraform.tfstate")
    print(subscription.name)
    ```
    """

    _terraform_type = "google_pubsub_subscription"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.id = self._attributes["id"]
