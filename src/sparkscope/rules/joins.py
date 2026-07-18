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