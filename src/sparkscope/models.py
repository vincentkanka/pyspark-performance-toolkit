from dataclasses import dataclass, field
from typing import Literal


Severity = Literal["LOW", "MEDIUM", "HIGH"]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: Severity
    title: str
    description: str
    recommendation: str


@dataclass(frozen=True)
class TableMetadata:
    name: str
    size_mb: float
    row_count: int
    partition_columns: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class JoinMetadata:
    left_table: str
    right_table: str
    join_type: str
    join_keys: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkloadMetadata:
    tables: list[TableMetadata]
    joins: list[JoinMetadata]