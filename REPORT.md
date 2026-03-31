# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### "What is the agentic loop?"

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

**The Loop:**
1. **Perceive** — Gather information from the environment (user input, tool outputs, file contents, API responses, etc.)
2. **Reason** — Process the information, plan next steps, and decide what action to take
3. **Act** — Execute the chosen action (call a tool, write a file, send a message, run a command, etc.)
4. **Observe** — Receive feedback from the action (success, error, output data)
5. **Repeat** — Use the new information to continue the loop until the goal is achieved

**Key Characteristics:**
- **Iterative:** The agent doesn't need all answers upfront—it learns and adapts as it goes
- **Goal-directed:** Each cycle moves toward completing an objective
- **Self-correcting:** Errors or unexpected results feed back into reasoning for adjustment
- **Autonomous:** The agent decides what to do next without step-by-step human guidance

This loop is what distinguishes an agent from a simple Q&A model—agents can take multiple steps, use tools, and adapt based on results rather than giving a single response.

### "What labs are available in our LMS?" (before MCP tools configured)

The agent responded with general knowledge about labs but could not access real LMS data. It attempted to use file system tools to explore the workspace but reported it couldn't access the LMS backend without proper authentication.

## Task 1B — Agent with LMS tools

### "What labs are available?"

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

### "Is the LMS backend healthy?"

Yes, the LMS backend is healthy! It currently has 56 items in the system.

## Task 1C — Skill prompt

### "Show me the scores" (without specifying a lab)

The agent correctly recognized that a lab parameter was needed and followed the skill strategy:

1. First said: "I'll check what labs are available in the LMS so you can choose which one to see scores for."
2. Called `lms_labs` tool to fetch available labs
3. Responded with:

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

The skill prompt successfully taught the agent to:
- Recognize when a lab parameter is missing
- Call `lms_labs` first to get available options
- Ask the user to choose before proceeding

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

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
