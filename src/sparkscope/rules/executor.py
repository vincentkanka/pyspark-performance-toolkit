from sparkscope.models import Finding


def check_executor_cores(config: dict[str, str]) -> list[Finding]:
    raw_value = config.get("spark.executor.cores")

    if raw_value is None:
        return []

    try:
        cores = int(raw_value)
    except ValueError:
        return [
            Finding(
                rule_id="EXECUTOR_CORES_INVALID",
                severity="MEDIUM",
                title="Executor cores setting is invalid",
                description="spark.executor.cores should be an integer value.",
                recommendation="Set spark.executor.cores to a valid integer.",
            )
        ]

    if cores > 5:
        return [
            Finding(
                rule_id="EXECUTOR_CORES_HIGH",
                severity="MEDIUM",
                title="Executor core count may be high",
                description=(
                    f"spark.executor.cores is set to {cores}. "
                    "High core counts per executor can increase garbage collection pressure "
                    "and reduce task isolation."
                ),
                recommendation=(
                    "Evaluate using fewer cores per executor, commonly in the 3–5 range, "
                    "depending on workload, memory, and cluster manager."
                ),
            )
        ]

    return []


def check_serializer(config: dict[str, str]) -> list[Finding]:
    serializer = config.get("spark.serializer", "")

    if serializer == "org.apache.spark.serializer.KryoSerializer":
        return []

    return [
        Finding(
            rule_id="JAVA_SERIALIZER_USED",
            severity="MEDIUM",
            title="JavaSerializer may reduce serialization performance",
            description=(
                "The default JavaSerializer can be slower and less compact for some Spark workloads."
            ),
            recommendation=(
                "Evaluate org.apache.spark.serializer.KryoSerializer for workloads with complex objects "
                "or heavy serialization overhead."
            ),
        )
    ]