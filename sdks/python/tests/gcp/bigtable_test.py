from terrabridge.gcp.bigtable import BigTableInstance, BigTableTable


def test_bigtable_instance():
    instance = BigTableInstance(
        resource_name="bigtable_instance", state_file="tests/data/terraform.tfstate"
    )

    assert instance.project == "terrabridge-testing"
    assert instance.name == "terrabridge-bigtable-instance"
    assert (
        instance.id
        == "projects/terrabridge-testing/instances/terrabridge-bigtable-instance"
    )


def test_bigtable_table():
    table = BigTableTable(
        resource_name="bigtable_table", state_file="tests/data/terraform.tfstate"
    )

    assert table.project == "terrabridge-testing"
    assert table.instance_name == "terrabridge-bigtable-instance"
    assert table.name == "tf-table"
    assert (
        table.id
        == "projects/terrabridge-testing/instances/terrabridge-bigtable-instance/tables/tf-table"
    )
    assert table.instance.project == "terrabridge-testing"
