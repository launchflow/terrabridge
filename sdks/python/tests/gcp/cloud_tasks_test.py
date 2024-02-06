from terrabridge.gcp.cloud_tasks import CloudTasksQueue


def test_cloud_tasks_queue():
    queue = CloudTasksQueue(
        resource_name="queue", state_file="tests/data/gcp/terraform.tfstate"
    )

    assert queue.project == "terrabridge-testing"
    assert queue.name == "cloud-tasks-queue-test"
    assert queue.id == (
        "projects/terrabridge-testing/locations/"
        "us-central1/queues/cloud-tasks-queue-test"
    )
