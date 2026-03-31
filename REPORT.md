# Lab 8 — Report

## Task 1A — Bare agent

### "What is the agentic loop?"

**Agent Response:**

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

1. **Perceive** — Gather information from the environment (user input, files, APIs, sensors, etc.)
2. **Reason/Plan** — Analyze the information, determine goals, and decide on a course of action
3. **Act** — Execute actions using available tools (file operations, API calls, shell commands, etc.)
4. **Observe** — Receive feedback from the actions taken (success, errors, new data)
5. **Iterate** — Loop back to reasoning based on observations until the goal is achieved

This loop enables agents to:
- Handle multi-step tasks
- Adapt to unexpected outcomes
- Self-correct based on feedback
- Work autonomously toward complex goals

### "What labs are available in our LMS?"

**Agent Response:**

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

## Task 1B — Agent with LMS tools

### "What labs are available?"

**Agent Response:**

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Is there a specific lab you'd like to explore or get data for?

### "Is the LMS backend healthy?"

**Agent Response:**

Yes, the LMS backend is healthy! It currently has 56 items in the system.

## Task 1C — Skill prompt

### "Show me the scores" (without specifying a lab)

**Agent Response:**

I'll check what labs are available in the LMS so you can choose which one to view scores for.

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Which lab would you like to see the scores for?

**Analysis:**

The skill prompt successfully taught the agent to:
- Recognize when a lab parameter is missing (user said "scores" without specifying which lab)
- Call `lms_labs` first to get available options
- Ask the user to choose before proceeding to fetch scores

## Task 2A — Deployed agent

### Nanobot Gateway Startup Log (from Docker container)

```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
WebChat channel enabled
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
Cron service started with 0 jobs
Heartbeat started (every 1800s)
Starting webchat channel...
Outbound dispatcher started
MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
MCP: registered tool 'mcp_lms_lms_learners' from server 'lms'
MCP: registered tool 'mcp_lms_lms_pass_rates' from server 'lms'
MCP: registered tool 'mcp_lms_lms_timeline' from server 'lms'
MCP: registered tool 'mcp_lms_lms_groups' from server 'lms'
MCP: registered tool 'mcp_lms_lms_top_learners' from server 'lms'
MCP: registered tool 'mcp_lms_lms_completion_rate' from server 'lms'
MCP: registered tool 'mcp_lms_lms_sync_pipeline' from server 'lms'
MCP server 'lms': connected, 9 tools registered
MCP: registered tool 'mcp_mcp_webchat_ui_message' from server 'mcp_webchat'
MCP server 'mcp_webchat': connected, 1 tools registered
Agent loop started
```

**Verification:**
- ✅ Nanobot service running in Docker
- ✅ WebChat channel enabled
- ✅ MCP servers connected (lms: 9 tools, mcp_webchat: 1 tool)
- ✅ Agent loop started successfully

## Task 2B — Web client

### Flutter Web Client

The Flutter web client is accessible at `http://localhost:42002/flutter/`

**HTML Response (verified):**
```html
<!DOCTYPE html>
<html>
<head>
  <base href="/flutter/">
  <meta charset="UTF-8">
  <title>Nanobot</title>
  ...
</head>
```

### WebSocket Endpoint Test

The WebSocket endpoint is accessible at `ws://localhost:42002/ws/chat?access_key=key`

**Agent Response from WebSocket (via Docker logs):**

```
User: "hello"
Agent: "Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?"
```

**Nanobot Gateway Full Logs:**
```
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
WebChat channel enabled
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
MCP server 'lms': connected, 9 tools registered
MCP server 'mcp_webchat': connected, 1 tools registered
Agent loop started
Processing message from webchat: hello
Response to webchat: Hello! 👋 I'm nanobot, your AI assistant. How can I help you today?
```

### Files Modified

- `nanobot-websocket-channel/` — Added as git submodule
- `nanobot/entrypoint.py` — Updated to configure webchat channel and mcp_webchat MCP server
- `nanobot/config.json` — Added webchat channel and mcp_webchat MCP server config
- `nanobot/Dockerfile` — Updated to install webchat dependencies
- `nanobot/workspace/skills/lms/SKILL.md` — Updated to use mcp_webchat_ui_message for structured UI
- `caddy/Caddyfile` — Enabled `/ws/chat` and `/flutter*` routes
- `docker-compose.yml` — Uncommented nanobot, client-web-flutter, and caddy config
- `pyproject.toml` — Added workspace members for webchat packages

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
