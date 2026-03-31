# mcp-obs

MCP server for observability (VictoriaLogs and VictoriaTraces).

## Usage

```bash
uv run python -m mcp_obs
```

## Environment Variables

- `NANOBOT_VICTORIALOGS_URL` - VictoriaLogs URL (default: http://localhost:42010)
- `NANOBOT_VICTORIATRACES_URL` - VictoriaTraces URL (default: http://localhost:42011)

## Tools

- `logs_search` - Search logs using LogsQL query
- `logs_error_count` - Count errors per service
- `traces_list` - List recent traces for a service
- `traces_get` - Fetch a specific trace by ID
