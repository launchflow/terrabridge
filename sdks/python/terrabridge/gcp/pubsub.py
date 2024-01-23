from typing import Optional

from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import pubsub_v1
except ImportError:
    pubsub_v1 = None


class PubSubTopic(GCPResource):
    """Represents a PubSub Topic

    Parsed from the terraform resource: `google_pubsub_topic`. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_topic>`.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import PubSubTopic

        topic = PubSubTopic("topic", state_file="gs://my-bucket/terraform.tfstate")
        print(topic.name)

        topic.publish(b"Hello, world!")

    Attributes:
        name (str): The name of the pub/sub topic.
    """

    _publisher = None
    _terraform_type = "google_pubsub_topic"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name = self._attributes["name"]

    def publish(self, message: bytes, ordering_key: str = "", **attributes):
        """Publish a message to the topic.

        Requires ``terrabridge[gcp]`` to be installed.
        """
        if pubsub_v1 is None:
            raise ImportError(
                "google-cloud-pubsub is not installed. "
                "Please install it with `pip install terrabridge[gcp]`."
            )
        if self._publisher is None:
            self._publisher = pubsub_v1.PublisherClient()
        return self._publisher.publish(
            topic=self.id, data=message, ordering_key=ordering_key, **attributes
        )


class PubSubSubscription(GCPResource):
    """Represents a PubSub Subscription

    Parsed from the terraform resource: ``google_pubsub_subscription``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_subscription>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import PubSubSubscription

        subscription = PubSubSubscription("subscription", state_file="gs://my-bucket/terraform.tfstate")
        print(subscription.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the pub/sub subscription.
    """

    _terraform_type = "google_pubsub_subscription"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.id = self._attributes["id"]
