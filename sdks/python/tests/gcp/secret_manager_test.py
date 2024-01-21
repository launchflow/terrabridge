from unittest.mock import patch

from terrabridge.gcp.secret_manager import SecretManagerSecret


def test_secret_manager_secret():
    secret = SecretManagerSecret(
        resource_name="secret",
        state_file="tests/data/terraform.tfstate",
    )

    assert secret.project == "terrabridge-testing"
    assert secret.name == "projects/717658685230/secrets/secret"
    assert secret.id == "projects/terrabridge-testing/secrets/secret"

    with patch("google.cloud.secretmanager.SecretManagerServiceClient") as mock:
        mock.return_value.access_secret_version.return_value.payload.data = b"secret"
        assert secret.version() == b"secret"
        mock.assert_called_once()
        mock.return_value.access_secret_version.assert_called_once_with(
            name="projects/717658685230/secrets/secret/versions/latest"
        )
