from typing import Any, Dict, Callable
from pydantic import BaseModel, ConfigDict, Field


class ToolResult(BaseModel):
    result: Any
    error: str | None = None


class SearchInput(BaseModel):
    query: str = Field(..., min_length=1)

    model_config = ConfigDict(extra="forbid")


class Tool(BaseModel):
    name: str
    description: str
    input_schema: type[BaseModel]
    func: Callable

    def execute(self, tool_input: Dict[str, Any]) -> ToolResult:
        # Strict validation against schema
        validated_input = self.input_schema(**tool_input)
        res = self.func(**validated_input.model_dump())
        return ToolResult(result=res)


def search_documents(query: str) -> str:
    return f"Search results for: {query}"


# Tool Registry
TOOL_REGISTRY: Dict[str, Tool] = {
    "search_documents": Tool(
        name="search_documents",
        description="Searches internal documents by query string.",
        input_schema=SearchInput,
        func=search_documents,
    )
}


def get_tool(name: str) -> Tool:
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' is not in the allowlist.")
    return TOOL_REGISTRY[name]