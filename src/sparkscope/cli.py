import json
from pathlib import Path

from sparkscope.analyzer import analyze_config


def analyze(config_path: str) -> None:
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a JSON object.")

    findings = analyze_config(config)

    if not findings:
        print("No findings detected.")
        return

    print("\nSparkScope Analysis Report")
    print("=" * 28)

    for finding in findings:
        print(f"\n[{finding.severity}] {finding.title}")
        print(f"Rule: {finding.rule_id}")
        print(f"Description: {finding.description}")
        print(f"Recommendation: {finding.recommendation}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog="sparkscope",
        description="Analyze Spark and PySpark workload configurations.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a Spark configuration JSON file.",
    )
    analyze_parser.add_argument(
        "config_path",
        help="Path to Spark configuration JSON file.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args.config_path)


if __name__ == "__main__":
    main()