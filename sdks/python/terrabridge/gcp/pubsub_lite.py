from typing import Dict
from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import pubsublite
except ImportError:
    pubsublite = None


class PubSubLiteTopic(GCPResource):
    """Represents a PubSub Lite Topic

    Parsed from the terraform resource: `google_pubsub_lite_topic`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_lite_topic).

    Example usage:

    ```python
    from terrabridge.gcp import PubSubLiteTopic

    topic = PubSubLiteTopic("lite_topic", state_file="gs://my-bucket/terraform.tfstate")
    print(topic.name)

    topic.publish(b"Hello, world!")
    ```
    """

    _terraform_type = "google_pubsub_lite_topic"
    _publisher = None

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name: str = self._attributes["name"]

    def publish(
        self, message: bytes, ordering_key: str = "", metadata: Dict[str, str] = {}
    ):
        if pubsublite is None:
            raise ImportError(
                "google-cloud-pubsub is not installed. Please install it with `pip install terrabridge[gcp]`."
            )
        if self._publisher is None:
            self._publisher = pubsublite.PublisherServiceClient()
        return self._publisher.publish(
            topic=self.id,
            data=message,
            ordering_key=ordering_key,
            metadata=list(metadata.items()),
        )


class PubSubLiteSubscription(GCPResource):
    """Represents a PubSub Lite Subscription

    Parsed from the terraform resource: `google_pubsub_lite_subscription`. For all
    available attributes, see the [Terraform documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_lite_subscription).

    Example usage:

    ```python
    from terrabridge.gcp import PubSubLiteSubscription

    sub = PubSubLiteSubscription("lite_subscription", state_file="gs://my-bucket/terraform.tfstate")
    print(sub.name)
    ```
    """

    _terraform_type = "google_pubsub_lite_subscription"

    def __init__(self, resource_name: str, *, state_file: str) -> None:
        super().__init__(resource_name, state_file=state_file)
        self.name = self._attributes["name"]
