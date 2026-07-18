import json

from sparkscope.cli import analyze, analyze_workload_file


def test_cli_analyze_outputs_config_findings(tmp_path, capsys):
    config = {
        "spark.sql.adaptive.enabled": "false",
        "spark.sql.shuffle.partitions": "2000",
        "spark.executor.cores": "8",
        "spark.serializer": "org.apache.spark.serializer.JavaSerializer",
    }

    config_path = tmp_path / "spark_config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    analyze(str(config_path))

    captured = capsys.readouterr()

    assert "SparkScope Configuration Analysis Report" in captured.out
    assert "Adaptive Query Execution is disabled" in captured.out
    assert "Shuffle partition count may be excessive" in captured.out


def test_cli_analyze_workload_outputs_findings(tmp_path, capsys):
    workload = {
        "tables": [
            {
                "name": "transactions",
                "size_mb": 50000,
                "row_count": 200000000,
                "partition_columns": ["transaction_date"],
            },
            {
                "name": "customers",
                "size_mb": 50,
                "row_count": 100000,
                "partition_columns": [],
            },
            {
                "name": "claims",
                "size_mb": 25000,
                "row_count": 80000000,
                "partition_columns": [],
            },
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

    workload_path = tmp_path / "spark_workload.json"
    workload_path.write_text(json.dumps(workload), encoding="utf-8")

    analyze_workload_file(str(workload_path))

    captured = capsys.readouterr()

    assert "SparkScope Workload Analysis Report" in captured.out
    assert "Broadcast join opportunity detected" in captured.out
    assert "Large table has no partition columns" in captured.out