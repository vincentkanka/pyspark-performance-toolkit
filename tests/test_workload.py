from sparkscope.workload import parse_workload_metadata


def test_parse_workload_metadata():
    data = {
        "tables": [
            {
                "name": "transactions",
                "size_mb": 50000,
                "row_count": 200000000,
                "partition_columns": ["transaction_date"],
            }
        ],
        "joins": [
            {
                "left_table": "transactions",
                "right_table": "customers",
                "join_type": "inner",
                "join_keys": ["customer_id"],
            }
        ],
    }

    workload = parse_workload_metadata(data)

    assert len(workload.tables) == 1
    assert workload.tables[0].name == "transactions"
    assert workload.tables[0].size_mb == 50000.0
    assert workload.tables[0].row_count == 200000000
    assert workload.tables[0].partition_columns == ["transaction_date"]

    assert len(workload.joins) == 1
    assert workload.joins[0].left_table == "transactions"
    assert workload.joins[0].right_table == "customers"
    assert workload.joins[0].join_type == "inner"
    assert workload.joins[0].join_keys == ["customer_id"]