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
- `cron` — Schedule recurring jobs (for proactive health checks).

## Strategy

### When user asks "What went wrong?" or "Check system health"

1. **Start with `logs_error_count`** for a recent time window (e.g., last 10 minutes)
2. **Use `logs_search`** to inspect the relevant service logs
   - Filter by service: `service.name:"Learning Management Service"`
   - Filter by severity: `severity:ERROR`
   - Filter by time: `_time:10m` (last 10 minutes)
   - Example query: `_time:10m service.name:"Learning Management Service" severity:ERROR`
3. **Extract `trace_id`** from relevant log entries
4. **Use `traces_get`** to fetch the full trace and understand the request flow
5. **Summarize findings** in one coherent explanation:
   - What service failed
   - What operation failed
   - What the error was
   - Evidence from both logs AND traces
   - Don't dump raw JSON — explain in plain language

### When user asks about errors in a time window

1. Call `logs_error_count` with the specified time range
2. If errors found, call `logs_search` to get details
3. Extract trace IDs and fetch traces if needed
4. Summarize: what failed, when, and what the traces show

### When user asks to create a health check

1. Use `cron` tool to schedule a recurring job
2. Each run should:
   - Call `logs_error_count` for the last 2 minutes
   - If errors found, call `logs_search` and `traces_get`
   - Post a short summary to the chat
3. Confirm the job was created

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
- **Cite both log AND trace evidence** when investigating failures
- **Name the affected service and the root failing operation**

## Examples

**User:** "What went wrong?"
**You:** 
1. Call `logs_error_count` with time_range="10m"
2. If errors found, call `logs_search` with query='_time:10m severity:ERROR'
3. Extract trace_id from results and call `traces_get`
4. Summarize: "The Learning Management Service failed during db_query operation. Logs show 'connection is closed' error. Trace ID xxx shows the request flow from auth_success to db_query failure."

**User:** "Any errors in the last hour?"
**You:** Call `logs_error_count` with time_range="1h", then summarize which services have errors

**User:** "Create a health check that runs every 2 minutes"
**You:** Use `cron` tool to schedule a job that calls `logs_error_count` for last 2 minutes and posts summary
