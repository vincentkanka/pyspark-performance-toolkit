from sparkscope.models import Finding, WorkloadMetadata
from sparkscope.rules.joins import check_broadcast_join_opportunities


def analyze_workload(workload: WorkloadMetadata) -> list[Finding]:
    findings: list[Finding] = []

    checks = [
        check_broadcast_join_opportunities,
    ]

    for check in checks:
        findings.extend(check(workload))

    return findings