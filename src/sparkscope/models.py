from dataclasses import dataclass
from typing import Literal


Severity = Literal["LOW", "MEDIUM", "HIGH"]


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: Severity
    title: str
    description: str
    recommendation: str