from typing import Optional

from terrabridge.aws.base import AWSResource

try:
    import boto3
    from mypy_boto3_s3.service_resource import Bucket
except ImportError:
    Bucket = object
    boto3 = None


class S3Bucket(AWSResource):
    """Represents a S3 Bucket

    Parsed from the terraform resource: ``aws_s3_bucket``. For all
    available attributes, see the `Terraform documentation <https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket>`_.

    Some attributes are pulled up to be top-level attributes for convenience for type hints.
    However all attributes that are available in the Terraform state file are available.

    Example
    -------
    .. code:: python

        from terrabridge.aws import S3Bucket

        # Load a S3 bucket from terraform state
        bucket = S3Bucket("bucket", state_file="terraform.tfstate")
        print(bucket.arn)

        # Fetch the remote bucket from boto3
        boto_bucket = bucket.fetch_bucket()
        print(boto_bucket.creation_date)

    Attributes:
        arn (str): The ARN assigned to the resource.
        id (str): The id of the resource.
        region (str): The region the resource belongs to.
        bucket (str): The name of the bucket.
    """

    _terraform_type = "aws_s3_bucket"
    _client = None

    def __init__(
        self,
        resource_name: str,
        *,
        module_name: Optional[str] = None,
        state_file: Optional[str] = None
    ) -> None:
        super().__init__(resource_name, module_name=module_name, state_file=state_file)
        self.bucket: str = self._attributes["bucket"]
        self.region = self._attributes["region"]

    def fetch_bucket(self) -> Bucket:
        """Fetches the bucket using boto3

        Returns:
            Bucket: The bucket object from boto3
        """
        if boto3 is None:
            raise ImportError(
                "boto3 is not installed. "
                "Please install it with `pip install terrabridge[aws]`."
            )
        if self._client is None:
            self._client = boto3.resource("s3")
        return self._client.Bucket(self.bucket)
