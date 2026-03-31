---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Use LMS MCP tools to provide live course analytics and data from the backend.

## Available Tools

- `lms_health` — Check if the LMS backend is healthy and report the item count. No parameters.
- `lms_labs` — List all labs available in the LMS. No parameters.
- `lms_learners` — List all learners registered in the LMS. No parameters.
- `lms_pass_rates` — Get pass rates (avg score and attempt count per task) for a lab. Requires `lab` parameter.
- `lms_timeline` — Get submission timeline (date + submission count) for a lab. Requires `lab` parameter.
- `lms_groups` — Get group performance (avg score + student count per group) for a lab. Requires `lab` parameter.
- `lms_top_learners` — Get top learners by average score for a lab. Requires `lab` and optional `limit` (default 5).
- `lms_completion_rate` — Get completion rate (passed / total) for a lab. Requires `lab` parameter.
- `lms_sync_pipeline` — Trigger the LMS sync pipeline. May take a moment. No parameters.

## Strategy

### When user asks for lab-specific data without naming a lab

If the user asks for scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. Call `lms_labs` first to get the list of available labs
2. If multiple labs are available, use the `mcp_webchat_ui_message` tool with `type: "choice"` to let the user pick one
3. Use each lab's `title` field as the choice label and `id` as the value
4. Once the user selects a lab, call the appropriate tool with the selected lab ID

### When user asks for general LMS info

- "What labs are available?" → Call `lms_labs` and list them
- "Is the backend healthy?" → Call `lms_health` and report status + item count
- "How many learners?" → Call `lms_learners` and report count
- "What can you do?" → Explain you can access live LMS data using the tools above

### Formatting responses

- Format percentages with one decimal place (e.g., "75.3%")
- Show counts as plain numbers (e.g., "56 items", "12 learners")
- For timelines, summarize the trend (e.g., "Most submissions occurred on...")
- For top learners, list names and scores in a numbered list

### Error handling

- If tools return 401 or connection errors, inform the user the LMS is unavailable
- Offer to trigger `lms_sync_pipeline` if data seems stale or missing
- If a lab ID is invalid, call `lms_labs` again and ask the user to choose from valid options

## Examples

**User:** "Show me the scores"
**You:** Call `lms_labs`, then present choices using `mcp_webchat_ui_message` with type "choice"

**User:** "Which lab has the lowest pass rate?"
**You:** Call `lms_labs`, then call `lms_pass_rates` for each lab, compare results, and report the lowest

**User:** "Show me the top 3 learners in lab-04"
**You:** Call `lms_top_learners` with lab="lab-04" and limit=3
