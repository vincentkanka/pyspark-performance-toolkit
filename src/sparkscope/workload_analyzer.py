from sparkscope.models import Finding, WorkloadMetadata
from sparkscope.rules.joins import check_broadcast_join_opportunities
from sparkscope.rules.partitions import check_large_unpartitioned_tables

def analyze_workload(workload: WorkloadMetadata) -> list[Finding]:
    findings: list[Finding] = []

    checks = [
        check_broadcast_join_opportunities,
        check_large_unpartitioned_tables,
    ]

    for check in checks:
        findings.extend(check(workload))

    return findings
