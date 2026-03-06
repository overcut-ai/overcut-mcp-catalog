# Package Registries Reference

## npm (for npx-based servers)

**Search:** `https://www.npmjs.com/search?q=mcp-server` or `npm search mcp-server`

**Common patterns:**
- Scoped: `@sentry/mcp-server`, `@brave/brave-search-mcp-server`
- Unscoped: `mcp-remote`, `mcp-grafana`

**serverConfig:**
```json
{
  "command": "npx",
  "args": ["-y", "@scope/package-name@latest"]
}
```

**Notes:**
- Always use `-y` to skip the install confirmation prompt
- Use `@latest` to ensure the newest version (optional but recommended)
- Some packages use `--package` flag: `["-y", "--package", "@scope/pkg", "--", "command", "start"]`

## PyPI (for uvx-based servers)

**Search:** `https://pypi.org/search/?q=mcp` or `pip search mcp`

**Common patterns:**
- `mcp-grafana`, `mcp-server-fetch`

**serverConfig:**
```json
{
  "command": "uvx",
  "args": ["package-name"]
}
```

**Notes:**
- No `-y` flag needed for uvx
- No `@latest` syntax — uvx resolves latest by default
- Requires `uv` to be installed on the host

## GitHub (for non-registry servers)

Some MCP servers aren't published to registries. Options:
1. Use `npx` with the GitHub URL: `npx -y github:org/repo`
2. Use `mcp-remote` if the server exposes an HTTP endpoint
3. Document as a custom setup (rare in catalog)

## mcp-remote (for HTTP/SSE endpoints)

**npm package:** `mcp-remote`

**When to use:**
- The MCP server is a hosted service with an HTTP/SSE endpoint
- No local package is published
- The vendor provides a URL-based MCP endpoint

**serverConfig:**
```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://api.example.com/mcp", "--header", "Authorization: Bearer ${TOKEN}"],
  "env": {
    "TOKEN": "${TOKEN}"
  }
}
```

**Notes:**
- The URL can contain `${VAR}` placeholders (e.g., `https://api.${DOMAIN}/mcp`)
- Auth headers are passed via `--header` flag
- Variables used in args should also appear in env for platform resolution
