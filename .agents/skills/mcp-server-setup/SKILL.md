---
name: MCP Server Setup
description: >
  Guide for finding, configuring, and testing MCP servers for catalog entries.
  Covers npx vs uvx, mcp-remote for HTTP endpoints, identifying required env vars,
  and common pitfalls. Use when adding new servers or debugging configurations.
---

# MCP Server Setup

This skill covers how to find MCP servers, determine their configuration, and add them to the catalog.

## Finding MCP Servers

1. **npm registry** — Search for `mcp-server` or `@scope/mcp-*` packages
2. **PyPI** — Search for `mcp-` prefixed packages (these use `uvx`)
3. **GitHub** — Search for repos with "mcp server" in the description
4. **MCP directories** — Check modelcontextprotocol.io and community lists
5. **Official vendor docs** — Many services now document their MCP server setup

## npx vs uvx Decision Tree

```
Is the package on npm?
  Yes -> Use npx: "command": "npx", "args": ["-y", "package-name"]
  No -> Is it on PyPI?
    Yes -> Use uvx: "command": "uvx", "args": ["package-name"]
    No -> Is it an HTTP/SSE endpoint?
      Yes -> Use mcp-remote (see below)
      No -> Custom command (rare)
```

**Key differences:**
- `npx` runs npm packages. Always include `-y` to auto-confirm install.
- `uvx` runs Python packages via uv. No `-y` flag needed.
- Both download and cache the package automatically.

## mcp-remote Pattern

For MCP servers exposed as HTTP/SSE endpoints (not local processes):

```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "<endpoint-url>", "--header", "Authorization: Bearer ${TOKEN}"],
  "env": {
    "TOKEN": "${TOKEN}"
  }
}
```

This uses the `mcp-remote` npm package to bridge HTTP endpoints to stdio. See `coralogix/` for a real example.

## Identifying Required Environment Variables

1. Check the upstream README/docs for configuration instructions
2. Look for `process.env.*` or `os.environ` in the server source code
3. Check existing Claude Desktop / MCP client config examples
4. Common patterns:
   - `*_API_KEY` or `*_ACCESS_TOKEN` — authentication
   - `*_URL` — service endpoint
   - `*_TEAM_ID` or `*_ORG_ID` — multi-tenant scoping

## Testing Locally

Before submitting a catalog entry, verify the server starts:

```bash
# npx-based
npx -y @scope/package-name@latest

# uvx-based
uvx package-name

# With env vars
SENTRY_ACCESS_TOKEN=test npx -y @sentry/mcp-server@latest
```

The server should start and listen on stdio without errors. It may print a "ready" message or simply wait for JSON-RPC input.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Wrong package name | Verify on npm/PyPI — exact scoped name matters |
| Missing `-y` in npx args | Always include: `["-y", "package"]` |
| Vars in args but not in env | If `${VAR}` appears in args, also add it to env for platform resolution |
| Empty env object | Use `"env": {}` not omitting the field, when vars are only in args |
| Version pinning | Prefer `@latest` for npx packages to stay current |
| Wrong env var name | Match the exact name the server expects (case-sensitive) |

See `references/package-registries.md` for more on package discovery.
