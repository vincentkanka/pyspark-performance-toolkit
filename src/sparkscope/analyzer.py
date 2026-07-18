from sparkscope.models import Finding
from sparkscope.rules.aqe import check_aqe_enabled
from sparkscope.rules.executor import check_executor_cores, check_serializer
from sparkscope.rules.partitions import check_shuffle_partitions


def analyze_config(config: dict[str, str]) -> list[Finding]:
    findings: list[Finding] = []

    checks = [
        check_aqe_enabled,
        check_shuffle_partitions,
        check_executor_cores,
        check_serializer,
    ]

    for check in checks:
        findings.extend(check(config))

    return findings