from sparkscope.models import Finding, WorkloadMetadata


BROADCAST_SIZE_THRESHOLD_MB = 100
LARGE_TABLE_SIZE_THRESHOLD_MB = 1000


def check_broadcast_join_opportunities(workload: WorkloadMetadata) -> list[Finding]:
    findings: list[Finding] = []
    tables_by_name = {table.name: table for table in workload.tables}

    for join in workload.joins:
        left_table = tables_by_name.get(join.left_table)
        right_table = tables_by_name.get(join.right_table)

        if left_table is None or right_table is None:
            continue

        if (
            left_table.size_mb >= LARGE_TABLE_SIZE_THRESHOLD_MB
            and right_table.size_mb <= BROADCAST_SIZE_THRESHOLD_MB
        ):
            findings.append(
                Finding(
                    rule_id="BROADCAST_JOIN_OPPORTUNITY",
                    severity="MEDIUM",
                    title="Broadcast join opportunity detected",
                    description=(
                        f"The table {right_table.name} is {right_table.size_mb:.1f} MB "
                        f"and is joined with larger table {left_table.name} "
                        f"({left_table.size_mb:.1f} MB)."
                    ),
                    recommendation=(
                        f"Evaluate broadcasting {right_table.name} to reduce shuffle during the join. "
                        "Validate with Spark UI metrics and workload testing."
                    ),
                )
            )

        elif (
            right_table.size_mb >= LARGE_TABLE_SIZE_THRESHOLD_MB
            and left_table.size_mb <= BROADCAST_SIZE_THRESHOLD_MB
        ):
            findings.append(
                Finding(
                    rule_id="BROADCAST_JOIN_OPPORTUNITY",
                    severity="MEDIUM",
                    title="Broadcast join opportunity detected",
                    description=(
                        f"The table {left_table.name} is {left_table.size_mb:.1f} MB "
                        f"and is joined with larger table {right_table.name} "
                        f"({right_table.size_mb:.1f} MB)."
                    ),
                    recommendation=(
                        f"Evaluate broadcasting {left_table.name} to reduce shuffle during the join. "
                        "Validate with Spark UI metrics and workload testing."
                    ),
                )
            )

    return findings

def check_join_key_partition_alignment(workload: WorkloadMetadata) -> list[Finding]:
    findings: list[Finding] = []
    tables_by_name = {table.name: table for table in workload.tables}

    for join in workload.joins:
        left_table = tables_by_name.get(join.left_table)
        right_table = tables_by_name.get(join.right_table)

        if left_table is None or right_table is None:
            continue

        for table in [left_table, right_table]:
            if not table.partition_columns or not join.join_keys:
                continue

            missing_keys = [
                join_key
                for join_key in join.join_keys
                if join_key not in table.partition_columns
            ]

            if missing_keys:
                findings.append(
                    Finding(
                        rule_id="JOIN_KEY_PARTITION_MISMATCH",
                        severity="LOW",
                        title="Join key does not align with partition columns",
                        description=(
                            f"The table {table.name} is partitioned by "
                            f"{', '.join(table.partition_columns)}, but the join uses "
                            f"{', '.join(join.join_keys)}."
                        ),
                        recommendation=(
                            "Review whether partitioning supports the most common join and filter patterns. "
                            "This does not always require changing partitioning, but it may indicate a shuffle risk."
                        ),
                    )
                )

    return findings