from unittest.mock import patch

from terrabridge.aws import S3Bucket


class _FakeBucket:
    pass


def test_s3_bucket():
    bucket = S3Bucket(
        resource_name="bucket",
        state_file="tests/data/aws/terraform.tfstate",
    )

    assert bucket.arn == "arn:aws:s3:::terrabridge-testing-bucket"
    assert bucket.id == "terrabridge-testing-bucket"
    assert bucket.region == "us-east-1"
    assert bucket.resource_name == "bucket"
    assert bucket.bucket == "terrabridge-testing-bucket"

    with patch("boto3.resource") as mock:
        to_ret = _FakeBucket()
        mock.return_value.Bucket.return_value = to_ret
        bucket = bucket.fetch_bucket()
        assert bucket == to_ret
        mock.assert_called_once()
        mock.return_value.Bucket.assert_called_once_with("terrabridge-testing-bucket")
