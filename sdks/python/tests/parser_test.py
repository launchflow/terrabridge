from terrabridge.gcp import GCSBucket
from terrabridge.parser import _parse_terraform_state

# NOTE: We don't test the local flow in this file because it's covered by
# all the other tests


def test_parse_gcs_state():
    _parse_terraform_state("gs://terrabridge-testing/terraform.tfstate")
    bucket = GCSBucket(
        "bucket", state_file="gs://terrabridge-testing/terraform.tfstate"
    )
    assert bucket.url == "gs://terrabridge-testing-terrabridge-testing"


def test_parse_s3_state():
    _parse_terraform_state("s3://terrabridge-testing/terraform.tfstate")
    bucket = GCSBucket(
        "bucket", state_file="s3://terrabridge-testing/terraform.tfstate"
    )
    assert bucket.url == "gs://terrabridge-testing-terrabridge-testing"
