from sparkscope.models import Finding


def print_findings(findings: list[Finding], report_title: str) -> None:
    if not findings:
        print("No findings detected.")
        return

    print(f"\n{report_title}")
    print("=" * len(report_title))

    for finding in findings:
        print(f"\n[{finding.severity}] {finding.title}")
        print(f"Rule: {finding.rule_id}")
        print(f"Description: {finding.description}")
        print(f"Recommendation: {finding.recommendation}")