from mock import patch

from terrabridge.gcp import GCSBucket

# TODO: add tests for reading bucket


class _FakeBucket:
    pass


def test_gcs_bucket():
    bucket = GCSBucket(
        resource_name="bucket",
        state_file="tests/data/terraform.tfstate",
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
