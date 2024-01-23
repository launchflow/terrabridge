from typing import Dict, Optional

from terrabridge.gcp.base import GCPResource

try:
    from google.cloud import pubsublite
except ImportError:
    pubsublite = None


class PubSubLiteTopic(GCPResource):
    """Represents a PubSub Lite Topic

    Parsed from the terraform resource: ``google_pubsub_lite_topic``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_lite_topic>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import PubSubLiteTopic

        topic = PubSubLiteTopic("lite_topic", state_file="gs://my-bucket/terraform.tfstate")
        print(topic.name)

        topic.publish(b"Hello, world!")

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the pub/sub lite topic.
    """

    _terraform_type = "google_pubsub_lite_topic"
    _publisher = None

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name: str = self._attributes["name"]

    def publish(
        self, message: bytes, ordering_key: str = "", metadata: Dict[str, str] = {}
    ):
        """Publish a message to the topic.

        Requires ``terrabridge[gcp]`` to be installed.
        """
        if pubsublite is None:
            raise ImportError(
                "google-cloud-pubsub is not installed. "
                "Please install it with `pip install terrabridge[gcp]`."
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
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/pubsub_lite_subscription>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.gcp import PubSubLiteSubscription

        sub = PubSubLiteSubscription("lite_subscription", state_file="gs://my-bucket/terraform.tfstate")
        print(sub.name)

    Attributes:
        project (str): The project the resource belongs to.
        id (str): The id of the resource.
        name (str): The name of the pub/sub lite subscription.
    """

    _terraform_type = "google_pubsub_lite_subscription"

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.name = self._attributes["name"]
