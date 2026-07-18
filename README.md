# SparkScope

SparkScope is an open-source performance analysis toolkit for Apache Spark and PySpark workloads.

It helps data engineers detect inefficient Spark configurations, excessive partitioning, expensive joins, missing Adaptive Query Execution settings, and other common performance bottlenecks before they become production incidents.

## Why SparkScope?

Spark performance problems are often discovered only after pipelines become slow, unstable, or expensive. Engineers then spend significant time reviewing Spark configurations, execution plans, event logs, and application behavior manually.

SparkScope aims to make this process more systematic by applying a documented set of performance assessment rules and producing clear, actionable recommendations.

## Initial Capabilities

SparkScope will analyze Spark configurations and identify issues such as:

* Adaptive Query Execution being disabled
* Excessive or insufficient shuffle partitions
* Potential broadcast join opportunities
* Inefficient executor memory and core configurations
* Missing Kryo serialization
* Common data-skew risks
* Potentially expensive shuffle operations

## Quick Start

Install locally for development:

```bash
python -m pip install -e ".[dev]"
```

Run SparkScope against the sample configuration:

```bash
sparkscope analyze examples/sample_config.json
```

Analyze workload metadata:

```bash
sparkscope analyze-workload examples/sample_workload.json
```

## Example

Input:

```json
{
  "spark.sql.adaptive.enabled": "false",
  "spark.sql.shuffle.partitions": "2000",
  "spark.executor.cores": "8",
  "spark.serializer": "org.apache.spark.serializer.JavaSerializer"
}
```

Expected output:

```text
HIGH: Adaptive Query Execution is disabled.
Recommendation: Enable spark.sql.adaptive.enabled for supported Spark workloads.

MEDIUM: The configured shuffle partition count may be excessive.
Recommendation: Review partition sizing based on shuffle volume and target partition size.

MEDIUM: Java serialization is configured.
Recommendation: Evaluate KryoSerializer for workloads containing complex objects.
```

## Project Roadmap

### Version 0.1.0 — Configuration Analyzer

* Analyze Spark configuration files
* Detect missing or inefficient settings
* Assign severity levels
* Produce terminal output
* Support JSON configuration input

### Version 0.2.0 — Join and Partition Analyzer

* Detect possible broadcast join opportunities
* Analyze partition counts
* Identify potential repartitioning problems
* Add structured JSON reports

### Version 0.3.0 — Spark Event Log Analysis

* Parse Spark event logs
* Identify slow stages
* Analyze task distribution
* Detect skew indicators
* Estimate shuffle overhead

### Version 0.4.0 — Reporting

* Generate HTML performance reports
* Rank recommendations by severity
* Add pipeline health scoring
* Add historical comparison support

### Version 1.0.0 — Complete Performance Assessment Framework

* Configuration analysis
* Event-log analysis
* Join analysis
* Partition analysis
* Performance scoring
* CLI and Python API
* Extensible rule engine

## Performance Assessment Methodology

SparkScope follows a five-stage assessment model:

1. Collect workload and configuration metadata
2. Evaluate configurations against performance rules
3. Detect likely bottlenecks and risks
4. Rank findings by severity and expected impact
5. Generate actionable engineering recommendations

The methodology will evolve as the project gains additional rules, workloads, benchmarks, and community feedback.

## Installation

SparkScope is currently under active development and is not yet available on PyPI.

Development installation instructions will be added with the first release.

## Contributing

Contributions, bug reports, performance rules, test cases, and documentation improvements are welcome.

See `CONTRIBUTING.md` for contribution guidelines.

## Disclaimer

SparkScope recommendations are diagnostic guidance. Spark performance depends on workload characteristics, data distribution, cluster configuration, infrastructure, and execution patterns. Recommendations should be validated through workload testing before production deployment.

## License

This project is licensed under the Apache License 2.0.
