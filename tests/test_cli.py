import json

from sparkscope.cli import analyze


def test_cli_analyze_outputs_findings(tmp_path, capsys):
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

    assert "SparkScope Analysis Report" in captured.out
    assert "Adaptive Query Execution is disabled" in captured.out
    assert "Shuffle partition count may be excessive" in captured.out