from sparkscope.analyzer import analyze_config


def test_analyzer_detects_common_issues():
    config = {
        "spark.sql.adaptive.enabled": "false",
        "spark.sql.shuffle.partitions": "2000",
        "spark.executor.cores": "8",
        "spark.serializer": "org.apache.spark.serializer.JavaSerializer",
    }

    findings = analyze_config(config)
    rule_ids = {finding.rule_id for finding in findings}

    assert "AQE_DISABLED" in rule_ids
    assert "SHUFFLE_PARTITIONS_HIGH" in rule_ids
    assert "EXECUTOR_CORES_HIGH" in rule_ids
    assert "JAVA_SERIALIZER_USED" in rule_ids


def test_analyzer_returns_no_aqe_finding_when_enabled():
    config = {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.shuffle.partitions": "200",
        "spark.executor.cores": "4",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    }

    findings = analyze_config(config)
    rule_ids = {finding.rule_id for finding in findings}

    assert "AQE_DISABLED" not in rule_ids