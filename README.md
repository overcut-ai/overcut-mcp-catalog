<a href="https://overcut.ai/#gh-light-mode-only">
  <img src="https://raw.githubusercontent.com/overcut-ai/overcut-playbooks/main/logo-overcut-black.svg" width="380">
</a>
<a href="https://overcut.ai/#gh-dark-mode-only">
  <img src="https://raw.githubusercontent.com/overcut-ai/overcut-playbooks/main/logo-overcut-white.svg" width="380">
</a>

# Overcut MCP Catalog

> Open-source catalog of pre-configured MCP (Model Context Protocol) server definitions for [Overcut](https://overcut.ai). Browse and install MCP servers with one click from the Overcut platform.

## What Is This?

This repository is the source of truth for the **MCP Server Catalog** in Overcut. Each directory contains a `catalog.json` file that defines an MCP server — its configuration, required secrets, and available tools. Overcut fetches this catalog and presents it as a browsable gallery, allowing users to install MCP servers without manually writing JSON configs.

## Quick Start

### For Overcut Users

1. Open your Overcut workspace
2. Navigate to **MCP Servers**
3. Click **Browse Catalog**
4. Find the MCP server you want and click **Install**
5. Provide any required secrets (API keys, tokens)
6. Done — the server is configured and ready to use

### For Contributors

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add new entries.

## Repository Structure

```
overcut-mcp-catalog/
  sentry/
    catalog.json        # Server definition
    icon.svg            # Server icon (optional)
  github/
    catalog.json
    icon.svg
  ...
```

Each directory name is the entry key (kebab-case). The only required file is `catalog.json`. An optional icon file (e.g., `icon.svg`) can be placed alongside it and referenced via `iconUrl` in the JSON.

## Catalog Entry Schema

Each `catalog.json` follows this schema:

```jsonc
{
  // Display metadata
  "name": "Sentry",                                         // Display name
  "description": "Search errors, investigate issues...",     // Short description
  "category": "monitoring",                                  // See categories below
  "tags": ["errors", "debugging"],                           // Searchable tags
  "iconUrl": "https://raw.githubusercontent.com/.../icon.svg", // Optional icon URL
  "websiteUrl": "https://github.com/getsentry/sentry-mcp",  // Optional docs link
  "priority": 10,                                            // Sort order (lower = first, default 100)

  // MCP server configuration (used as-is by Overcut)
  "serverConfig": {
    "command": "npx",
    "args": ["-y", "@sentry/mcp-server@latest"],
    "env": {
      "SENTRY_ACCESS_TOKEN": "${SENTRY_ACCESS_TOKEN}"
    }
  },

  // Secrets the user must provide
  "requiredSecrets": [
    {
      "envVar": "SENTRY_ACCESS_TOKEN",           // Must match ${VAR} in serverConfig.env
      "displayName": "Sentry Access Token",       // Shown in the install dialog
      "description": "Create an Internal Integration token...",
      "helpUrl": "https://docs.sentry.io/..."     // Optional link to docs
    }
  ],

  // Tool allowlists
  "recommendedTools": ["search_errors", "get_issue"],  // Pre-selected on install
  "allTools": ["search_errors", "get_issue", "..."]    // Full list, user can toggle
}
```

### Categories

| Value | Description |
|-------|-------------|
| `developer-tools` | Git, CI/CD, code analysis, IDEs |
| `productivity` | Project management, task tracking |
| `data` | Search, databases, analytics |
| `monitoring` | Error tracking, observability, APM |
| `communication` | Chat, email, notifications |
| `ai` | AI/ML services, LLM tools |
| `other` | Anything that doesn't fit above |

### Key Rules

- `serverConfig` must be a valid MCP server config (`{command, args, env}` for stdio or `{url, headers}` for SSE)
- Every `${VAR}` placeholder in `serverConfig.env` must have a matching entry in `requiredSecrets`
- If `requiredSecrets` is empty, no secrets are prompted during install (e.g., filesystem server)
- `recommendedTools` is a subset of `allTools`

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Adding a New MCP Server

1. Create a directory with the server name in kebab-case
2. Add a `catalog.json` following the schema above
3. Optionally add an `icon.svg` (square, simple, works on dark backgrounds)
4. Submit a pull request

## Links

- [Overcut Platform](https://overcut.ai)
- [Overcut Documentation](https://docs.overcut.ai)
- [MCP Specification](https://modelcontextprotocol.io)

## License

Apache License 2.0 - See [LICENSE](./LICENSE) for details.
