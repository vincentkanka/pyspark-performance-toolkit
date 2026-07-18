# Usage

SparkScope provides a command-line interface for analyzing Spark configuration files.

## Analyze a Spark Configuration

Run:

```bash
sparkscope analyze examples/sample_config.json

```markdown
## Analyze Workload Metadata
```
SparkScope can also analyze workload metadata for join and partition risks.

Run:

```bash
sparkscope analyze-workload examples/sample_workload.json
```