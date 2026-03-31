---
name: observability
description: Use observability tools to investigate errors and traces
always: true
---

# Observability Skill

Use VictoriaLogs and VictoriaTraces MCP tools to investigate system errors and trace request flows.

## Available Tools

- `logs_search` — Search VictoriaLogs using LogsQL query. Use fields like `service.name`, `severity`, `event`, `trace_id`.
- `logs_error_count` — Count errors per service over a time window.
- `traces_list` — List recent traces for a service from VictoriaTraces.
- `traces_get` — Fetch a specific trace by ID.

## Strategy

### When user asks about errors

1. **Start with `logs_error_count`** to see if there are recent errors and which services are affected
2. **Use `logs_search`** to inspect the relevant service logs
   - Filter by service: `service.name:"Learning Management Service"`
   - Filter by severity: `severity:ERROR`
   - Filter by time: `_time:10m` (last 10 minutes)
   - Example query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
3. **Extract `trace_id`** from relevant log entries
4. **Use `traces_get`** to fetch the full trace and understand the request flow
5. **Summarize findings** concisely — don't dump raw JSON

### When user asks about a specific service

1. Use `logs_search` with the service name filter
2. Look for error patterns or slow operations
3. If you find issues, extract trace IDs and fetch full traces

### Query patterns

**Find recent errors:**
```
_time:10m severity:ERROR
```

**Find errors for specific service:**
```
_time:10m service.name:"Learning Management Service" severity:ERROR
```

**Find logs with specific trace:**
```
trace_id:264f6f313185254fee3fa300bbccd3c1
```

## Response style

- **Be concise** — summarize findings, don't dump raw JSON
- **Include timestamps** — when did the error occur?
- **Include trace IDs** — so the user can look up full traces in the UI
- **Explain the impact** — what functionality is affected?
- **Suggest next steps** — if appropriate

## Examples

**User:** "Any errors in the last hour?"
**You:** Call `logs_error_count` with time_range="1h", then summarize which services have errors

**User:** "Any LMS backend errors in the last 10 minutes?"
**You:** 
1. Call `logs_error_count` with time_range="10m", service="Learning Management Service"
2. If errors found, call `logs_search` with query='_time:10m service.name:"Learning Management Service" severity:ERROR'
3. Extract trace_id from results and call `traces_get` if needed
4. Summarize: what failed, when, and what trace shows

**User:** "Show me the trace for request abc123"
**You:** Call `traces_get` with trace_id="abc123" and summarize the span hierarchy
