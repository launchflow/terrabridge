from unittest.mock import patch

import terrabridge
from terrabridge.gcp import GCSBucket


class _FakeBucket:
    pass


def test_gcs_bucket():
    bucket = GCSBucket(
        resource_name="bucket",
        state_file="tests/data/gcp/terraform.tfstate",
    )

    assert bucket.project == "terrabridge-testing"
    assert bucket.url == "gs://terrabridge-testing-terrabridge-testing"
    assert bucket.resource_name == "bucket"
    assert bucket.name == "terrabridge-testing-terrabridge-testing"

    with patch("google.cloud.storage.Client") as mock:
        to_ret = _FakeBucket()
        mock.return_value.get_bucket.return_value = to_ret
        assert bucket.bucket() == to_ret
        mock.assert_called_once()
        mock.return_value.get_bucket.assert_called_once_with(
            "terrabridge-testing-terrabridge-testing"
        )


def test_gcs_bucket_module():
    bucket = GCSBucket(
        resource_name="bucket",
        state_file="tests/data/gcp/terraform.tfstate",
        module_name="module.bucket",
    )

    assert bucket.project == "terrabridge-testing"
    assert bucket.url == "gs://terrabridge-testing-terrabridge-testing-module"
    assert bucket.resource_name == "bucket"
    assert bucket.name == "terrabridge-testing-terrabridge-testing-module"


def test_gcs_bucket_global_state_file():
    try:
        terrabridge.state_file = "tests/data/gcp/terraform.tfstate"
        bucket = GCSBucket(resource_name="bucket")

        assert bucket.url == "gs://terrabridge-testing-terrabridge-testing"
    finally:
        terrabridge.state_file = None


def test_gcs_bucket_global_no_state_file():
    try:
        GCSBucket(resource_name="bucket")
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
