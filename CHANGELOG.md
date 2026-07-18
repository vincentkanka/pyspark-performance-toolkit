# Changelog

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