from terrabridge.gcp.bigquery import BigQueryDataset, BigQueryTable


def test_bigquery_dataset():
    dataset = BigQueryDataset(
        resource_name="dataset", state_file="tests/data/terraform.tfstate"
    )

    assert dataset.project == "terrabridge-testing"
    assert dataset.dataset_id == "terrabridge_testing_dataset"
    assert dataset.id == (
        "projects/terrabridge-testing/" "datasets/terrabridge_testing_dataset"
    )


def test_bigquery_table():
    table = BigQueryTable(
        resource_name="table", state_file="tests/data/terraform.tfstate"
    )

    assert table.project == "terrabridge-testing"
    assert table.dataset_id == "terrabridge_testing_dataset"
    assert table.table_id == "terrabridge-testing-table"
    assert table.id == (
        "projects/terrabridge-testing/datasets/"
        "terrabridge_testing_dataset/tables/terrabridge-testing-table"
    )
    assert table.dataset.project == "terrabridge-testing"
    assert False


def test_type_mismatch():
    try:
        BigQueryTable(
            resource_name="bigtable_table", state_file="tests/data/terraform.tfstate"
        )
    except ValueError:
        return
    assert False, "Expected ValueError"
