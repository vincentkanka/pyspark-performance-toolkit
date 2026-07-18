# Changelog
## v0.2.0 - Join and Partition Analyzer

### Added
- Workload metadata models for tables and joins
- Workload metadata parser
- Workload analyzer
- Broadcast join opportunity detection
- Large unpartitioned table detection
- Join key and partition alignment detection
- CLI command for workload analysis
- Sample workload metadata file
- Unit tests for workload analysis

### Notes
This release expands SparkScope from static Spark configuration analysis into workload metadata analysis. It introduces the first join and partition analysis capabilities and lays the foundation for future Spark event log and execution-plan analysis.

## v0.1.0 - Initial Configuration Analyzer

### Added
- Initial Spark configuration analyzer
- Rule engine for evaluating Spark configuration settings
- AQE disabled detection
- Shuffle partition validation
- Executor core validation
- Serializer recommendation
- CLI command for analyzing JSON configuration files
- Unit tests for analyzer and CLI
- Example Spark configuration file

### Notes
This release focuses on static Spark configuration analysis. Future releases will add join analysis, partition analysis, Spark event log parsing, and HTML reports.