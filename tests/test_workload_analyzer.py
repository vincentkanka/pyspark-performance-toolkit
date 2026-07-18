from sparkscope.models import JoinMetadata, TableMetadata, WorkloadMetadata
from sparkscope.workload_analyzer import analyze_workload


def test_detects_broadcast_join_opportunity():
    workload = WorkloadMetadata(
        tables=[
            TableMetadata(
                name="transactions",
                size_mb=50000,
                row_count=200000000,
                partition_columns=["transaction_date"],
            ),
            TableMetadata(
                name="customers",
                size_mb=50,
                row_count=100000,
                partition_columns=[],
            ),
        ],
        joins=[
            JoinMetadata(
                left_table="transactions",
                right_table="customers",
                join_type="inner",
                join_keys=["customer_id"],
            )
        ],
    )

    findings = analyze_workload(workload)
    rule_ids = {finding.rule_id for finding in findings}

    assert "BROADCAST_JOIN_OPPORTUNITY" in rule_ids


def test_no_broadcast_finding_for_two_large_tables():
    workload = WorkloadMetadata(
        tables=[
            TableMetadata(
                name="transactions",
                size_mb=50000,
                row_count=200000000,
                partition_columns=["transaction_date"],
            ),
            TableMetadata(
                name="claims",
                size_mb=25000,
                row_count=80000000,
                partition_columns=["claim_date"],
            ),
        ],
        joins=[
            JoinMetadata(
                left_table="transactions",
                right_table="claims",
                join_type="inner",
                join_keys=["policy_id"],
            )
        ],
    )

    findings = analyze_workload(workload)
    rule_ids = {finding.rule_id for finding in findings}

    assert "BROADCAST_JOIN_OPPORTUNITY" not in rule_ids