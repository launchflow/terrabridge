from terrabridge.gcp import GCSBucket

bucket = GCSBucket("bucket", state_file="terraform.tfstate")
bucket = bucket.bucket()
print(bucket.get_iam_policy().bindings)
