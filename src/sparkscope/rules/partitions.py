from sparkscope.models import Finding, WorkloadMetadata

LARGE_UNPARTITIONED_TABLE_THRESHOLD_MB = 10000

def check_shuffle_partitions(config: dict[str, str]) -> list[Finding]:
    raw_value = config.get("spark.sql.shuffle.partitions")

    if raw_value is None:
        return [
            Finding(
                rule_id="SHUFFLE_PARTITIONS_DEFAULT",
                severity="LOW",
                title="Shuffle partitions setting is not explicitly configured",
                description=(
                    "Spark defaults spark.sql.shuffle.partitions to 200. "
                    "This may be too high for small workloads or too low for large workloads."
                ),
                recommendation=(
                    "Set spark.sql.shuffle.partitions based on shuffle data size, cluster resources, "
                    "and target partition size."
                ),
            )
        ]

    try:
        partitions = int(raw_value)
    except ValueError:
        return [
            Finding(
                rule_id="SHUFFLE_PARTITIONS_INVALID",
                severity="MEDIUM",
                title="Shuffle partitions setting is invalid",
                description="spark.sql.shuffle.partitions should be an integer value.",
                recommendation="Set spark.sql.shuffle.partitions to a valid integer.",
            )
        ]

    if partitions > 1000:
        return [
            Finding(
                rule_id="SHUFFLE_PARTITIONS_HIGH",
                severity="MEDIUM",
                title="Shuffle partition count may be excessive",
                description=(
                    f"spark.sql.shuffle.partitions is set to {partitions}. "
                    "Excessive partition counts can increase scheduling overhead and create many small tasks."
                ),
                recommendation=(
                    "Review shuffle volume and target partition size. Consider reducing partition count "
                    "or enabling Adaptive Query Execution."
                ),
            )
        ]

    if partitions < 20:
        return [
            Finding(
                rule_id="SHUFFLE_PARTITIONS_LOW",
                severity="MEDIUM",
                title="Shuffle partition count may be too low",
                description=(
                    f"spark.sql.shuffle.partitions is set to {partitions}. "
                    "Too few partitions may reduce parallelism and create large shuffle tasks."
                ),
                recommendation=(
                    "Increase shuffle partitions based on cluster size, shuffle volume, "
                    "and target task duration."
                ),
            )
        ]

    return []

def check_large_unpartitioned_tables(workload: WorkloadMetadata) -> list[Finding]:
    findings: list[Finding] = []

    for table in workload.tables:
        if table.size_mb >= LARGE_UNPARTITIONED_TABLE_THRESHOLD_MB and not table.partition_columns:
            findings.append(
                Finding(
                    rule_id="LARGE_UNPARTITIONED_TABLE",
                    severity="MEDIUM",
                    title="Large table has no partition columns",
                    description=(
                        f"The table {table.name} is {table.size_mb:.1f} MB "
                        "but has no partition columns defined."
                    ),
                    recommendation=(
                        "Evaluate partitioning strategy based on common filter columns, "
                        "data freshness requirements, and query access patterns."
                    ),
                )
            )

    return findings