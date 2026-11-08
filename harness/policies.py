from enum import Enum
from typing import Dict


class PermissionLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    DESTRUCTIVE = "DESTRUCTIVE"


TOOL_PERMISSIONS: Dict[str, PermissionLevel] = {
    "search_documents": PermissionLevel.READ_ONLY,
    "delete_database": PermissionLevel.DESTRUCTIVE,
    "drop_table": PermissionLevel.DESTRUCTIVE,
}


def check_tool_permission(tool_name: str) -> PermissionLevel:
    return TOOL_PERMISSIONS.get(tool_name, PermissionLevel.DESTRUCTIVE)