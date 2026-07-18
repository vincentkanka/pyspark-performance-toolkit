from typing import Any

from sparkscope.models import JoinMetadata, TableMetadata, WorkloadMetadata


def parse_workload_metadata(data: dict[str, Any]) -> WorkloadMetadata:
    tables = [
        TableMetadata(
            name=table["name"],
            size_mb=float(table["size_mb"]),
            row_count=int(table["row_count"]),
            partition_columns=list(table.get("partition_columns", [])),
        )
        for table in data.get("tables", [])
    ]

    joins = [
        JoinMetadata(
            left_table=join["left_table"],
            right_table=join["right_table"],
            join_type=join["join_type"],
            join_keys=list(join.get("join_keys", [])),
        )
        for join in data.get("joins", [])
    ]

    return WorkloadMetadata(tables=tables, joins=joins)