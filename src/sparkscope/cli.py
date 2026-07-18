import json
from pathlib import Path
from typing import Any

from sparkscope.analyzer import analyze_config
from sparkscope.findings import print_findings
from sparkscope.workload import parse_workload_metadata
from sparkscope.workload_analyzer import analyze_workload


def load_json_file(file_path: str) -> dict[str, Any]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Input file must contain a JSON object.")

    return data


def analyze(config_path: str) -> None:
    config = load_json_file(config_path)
    findings = analyze_config(config)
    print_findings(findings, "SparkScope Configuration Analysis Report")


def analyze_workload_file(workload_path: str) -> None:
    data = load_json_file(workload_path)
    workload = parse_workload_metadata(data)
    findings = analyze_workload(workload)
    print_findings(findings, "SparkScope Workload Analysis Report")


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

    workload_parser = subparsers.add_parser(
        "analyze-workload",
        help="Analyze Spark workload metadata JSON file.",
    )
    workload_parser.add_argument(
        "workload_path",
        help="Path to Spark workload metadata JSON file.",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        analyze(args.config_path)
    elif args.command == "analyze-workload":
        analyze_workload_file(args.workload_path)


if __name__ == "__main__":
    main()