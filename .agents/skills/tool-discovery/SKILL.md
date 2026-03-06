---
name: Tool Discovery
description: >
  Methods for discovering and documenting MCP server tools, choosing
  recommendedTools, and keeping tool lists accurate. Use when populating
  allTools and recommendedTools for catalog entries.
---

# Tool Discovery

Each catalog entry lists tools in `allTools` (complete set) and `recommendedTools` (pre-selected subset). This skill covers how to discover and document them accurately.

## Discovery Methods (in order of reliability)

### 1. Upstream documentation
- Check the MCP server's README, docs site, or GitHub wiki
- Look for a "Tools" or "Available Tools" section
- Most reliable when the docs are up-to-date

### 2. MCP Inspector
- Run the server locally and use the MCP Inspector to list tools:
  ```bash
  npx @anthropic-ai/mcp-inspector npx -y @scope/package-name
  ```
- This connects to the running server and queries `tools/list`
- Shows exact tool names, descriptions, and parameters

### 3. Source code
- Search for `server.tool(` or `@server.list_tools` patterns
- Look for tool registration in the server's main entry point
- Tool names are usually string literals in the registration call

### 4. Claude Desktop / MCP client
- Configure the server in Claude Desktop's `claude_desktop_config.json`
- Open a conversation and check which tools appear
- Useful for verifying tool names match what the client sees

## Tool Naming

- Use the **exact** tool names as exposed by the server
- Tool names are typically `snake_case` (e.g., `search_errors`, `get_issue_details`)
- Some servers use `kebab-case` (e.g., `list-feature-flags`) — match whatever the server uses
- Some servers prefix tools (e.g., `slack_list_channels`, `brave_web_search`)
- Never rename or normalize tool names — they must match exactly

## Choosing recommendedTools

**Guidelines:**
- Select **3-6** tools that cover the server's primary use cases
- **Prefer read/query operations** over write/create/delete
- Include the tools a user would most likely need in their first session
- Skip admin, config, and destructive tools

**Decision framework:**
1. What are the top 3 things users want to do with this server?
2. Which tools enable those use cases?
3. Add 1-2 more for common secondary needs

**Examples:**
- Sentry: `search_events`, `get_issue_details`, `find_projects`, `find_organizations` (core investigation flow)
- Grafana: `search_dashboards`, `query_prometheus`, `query_loki_logs`, `list_alert_rules`, `list_incidents`, `list_oncall_schedules` (covers all major features)
- Slack: `slack_list_channels`, `slack_post_message`, `slack_get_channel_history` (read + write basics)

## Keeping Lists Current

MCP servers evolve. When updating an entry:
1. Re-run discovery (MCP Inspector or upstream docs)
2. Add new tools to `allTools`
3. Remove tools that no longer exist
4. Check if `recommendedTools` should be updated
5. Run `python3 scripts/validate-catalog.py {entry-name}` to verify

## Verification Checklist

- [ ] All tool names match the server's actual tool names exactly
- [ ] No duplicate entries in `allTools` or `recommendedTools`
- [ ] Every `recommendedTools` entry exists in `allTools`
- [ ] Tool count is reasonable (cross-check with upstream docs)
- [ ] Validation script passes
