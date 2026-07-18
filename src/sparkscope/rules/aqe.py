from sparkscope.models import Finding


def check_aqe_enabled(config: dict[str, str]) -> list[Finding]:
    value = config.get("spark.sql.adaptive.enabled", "").lower()

    if value == "true":
        return []

    return [
        Finding(
            rule_id="AQE_DISABLED",
            severity="HIGH",
            title="Adaptive Query Execution is disabled",
            description=(
                "Adaptive Query Execution can improve Spark SQL workloads by "
                "dynamically optimizing shuffle partitions, skew joins, and join strategies."
            ),
            recommendation=(
                "Enable spark.sql.adaptive.enabled for supported Spark SQL workloads "
                "and validate performance with representative data."
            ),
        )
    ]