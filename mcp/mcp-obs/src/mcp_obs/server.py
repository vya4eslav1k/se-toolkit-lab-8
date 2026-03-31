"""MCP server for observability (VictoriaLogs and VictoriaTraces)."""

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field


class LogsSearchParams(BaseModel):
    """Search logs by query and time range."""
    query: str = Field(description="LogsQL query string")
    limit: int = Field(default=10, description="Max results to return")


class LogsErrorCountParams(BaseModel):
    """Count errors per service over a time window."""
    time_range: str = Field(default="1h", description="Time range (e.g., '1h', '10m')")
    service: str = Field(default="", description="Filter by service name (optional)")


class TracesListParams(BaseModel):
    """List recent traces for a service."""
    service: str = Field(description="Service name")
    limit: int = Field(default=5, description="Max traces to return")


class TracesGetParams(BaseModel):
    """Fetch a specific trace by ID."""
    trace_id: str = Field(description="Trace ID")


ToolPayload = BaseModel | list[BaseModel]


def _text(data: Any) -> list[TextContent]:
    """Convert data to text content."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    elif isinstance(data, list):
        payload = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, indent=2, ensure_ascii=False))]


class ObservabilityClient:
    """Client for VictoriaLogs and VictoriaTraces APIs."""

    def __init__(self, victorialogs_url: str, victoriatraces_url: str):
        self.victorialogs_url = victorialogs_url.rstrip("/")
        self.victoriatraces_url = victoriatraces_url.rstrip("/")

    async def logs_search(self, query: str, limit: int = 10) -> list[dict]:
        """Search logs using LogsQL query."""
        async with httpx.AsyncClient() as client:
            url = f"{self.victorialogs_url}/select/logsql/query"
            params = {"query": query, "limit": limit}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            # VictoriaLogs returns newline-delimited JSON
            lines = response.text.strip().split("\n")
            results = []
            for line in lines:
                if line.strip():
                    try:
                        results.append(json.loads(line))
                    except json.JSONDecodeError:
                        results.append({"_msg": line})
            return results

    async def logs_error_count(self, time_range: str = "1h", service: str = "") -> list[dict]:
        """Count errors per service over a time window."""
        query = f"_time:{time_range} severity:ERROR"
        if service:
            query += f' service.name:"{service}"'
        results = await self.logs_search(query, limit=1000)
        # Count by service
        counts: dict[str, int] = {}
        for result in results:
            stream = result.get("_stream", "")
            # Extract service.name from stream
            if 'service.name="' in stream:
                start = stream.find('service.name="') + len('service.name="')
                end = stream.find('"', start)
                if end > start:
                    svc = stream[start:end]
                    counts[svc] = counts.get(svc, 0) + 1
        return [{"service": svc, "error_count": count} for svc, count in sorted(counts.items(), key=lambda x: -x[1])]

    async def traces_list(self, service: str, limit: int = 5) -> dict:
        """List recent traces for a service."""
        async with httpx.AsyncClient() as client:
            url = f"{self.victoriatraces_url}/select/jaeger/api/traces"
            params = {"service": service, "limit": limit}
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()

    async def traces_get(self, trace_id: str) -> dict:
        """Fetch a specific trace by ID."""
        async with httpx.AsyncClient() as client:
            url = f"{self.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()


def create_server(client: ObservabilityClient) -> Server:
    """Create the MCP server with observability tools."""
    server = Server("mcp-obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="logs_search",
                description="Search VictoriaLogs using LogsQL query. Use fields like service.name, severity, event, trace_id. Example: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
                inputSchema=LogsSearchParams.model_json_schema(),
            ),
            Tool(
                name="logs_error_count",
                description="Count errors per service over a time window. Returns list of services with error counts.",
                inputSchema=LogsErrorCountParams.model_json_schema(),
            ),
            Tool(
                name="traces_list",
                description="List recent traces for a service from VictoriaTraces.",
                inputSchema=TracesListParams.model_json_schema(),
            ),
            Tool(
                name="traces_get",
                description="Fetch a specific trace by ID. Use trace_id from logs to get full trace details.",
                inputSchema=TracesGetParams.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        args = arguments or {}
        try:
            if name == "logs_search":
                params = LogsSearchParams.model_validate(args)
                results = await client.logs_search(params.query, params.limit)
                return _text(results)
            elif name == "logs_error_count":
                params = LogsErrorCountParams.model_validate(args)
                results = await client.logs_error_count(params.time_range, params.service)
                return _text(results)
            elif name == "traces_list":
                params = TracesListParams.model_validate(args)
                results = await client.traces_list(params.service, params.limit)
                return _text(results)
            elif name == "traces_get":
                params = TracesGetParams.model_validate(args)
                results = await client.traces_get(params.trace_id)
                return _text(results)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    return server


async def main() -> None:
    """Main entry point."""
    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://localhost:42010")
    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://localhost:42011")

    client = ObservabilityClient(victorialogs_url, victoriatraces_url)
    server = create_server(client)

    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
