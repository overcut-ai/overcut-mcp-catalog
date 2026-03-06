---
name: Catalog Schema Reference
description: >
  Deep-dive reference for the catalog.json schema — field types, constraints,
  valid categories, serverConfig patterns, requiredSecrets conventions, and
  recommendedTools selection guidance. Use when creating or editing catalog entries.
---

# Catalog Schema Reference

Every MCP server entry in this catalog is defined by a single `catalog.json` file inside a kebab-case directory. This skill covers the complete schema.

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable display name (e.g., "Brave Search") |
| `description` | string | Yes | 1-2 sentence summary of what the server does |
| `category` | string | Yes | One of the valid categories (see below) |
| `tags` | string[] | No | Searchable keywords for discovery |
| `iconUrl` | string | No | URL to the server icon (see icon-guidelines skill) |
| `websiteUrl` | string | No | Link to upstream docs, repo, or homepage |
| `priority` | number | No | Sort order; lower = shown first. Default: 100 |
| `serverConfig` | object | Yes | MCP server configuration object |
| `requiredSecrets` | object[] | No | Secrets the user must provide during install |
| `recommendedTools` | string[] | No | Tools pre-selected on install (subset of allTools) |
| `allTools` | string[] | No | Complete list of tools the server exposes |

See `references/field-reference.md` for exhaustive field documentation.

## Valid Categories

| Value | Description | Example Entries |
|-------|-------------|-----------------|
| `developer-tools` | Git, CI/CD, code analysis, feature flags | langsmith, launchdarkly |
| `productivity` | Project management, task tracking | (none yet) |
| `data` | Search, databases, analytics | brave-search, elasticsearch |
| `monitoring` | Error tracking, observability, APM | sentry, grafana, datadog, coralogix, cloudwatch, new-relic, splunk |
| `communication` | Chat, email, notifications | slack |
| `design` | UI/UX design tools | figma |
| `documentation` | Knowledge bases, wikis, docs platforms | confluence, notion |
| `incident-management` | Incident response, alerting, on-call | opsgenie, pagerduty |
| `it-service-management` | ITSM, ticketing, service desks | servicenow |
| `ai` | AI/ML services, LLM tools | (none yet) |
| `other` | Anything that doesn't fit above | (none yet) |

## serverConfig Patterns

### stdio via npx (most common)

```json
{
  "command": "npx",
  "args": ["-y", "@scope/package-name@latest"],
  "env": {
    "API_KEY": "${API_KEY}"
  }
}
```

### stdio via uvx (Python packages)

```json
{
  "command": "uvx",
  "args": ["package-name"],
  "env": {
    "SERVICE_URL": "${SERVICE_URL}",
    "SERVICE_TOKEN": "${SERVICE_TOKEN}"
  }
}
```

### mcp-remote (HTTP/SSE endpoints)

```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://api.${DOMAIN}/mcp", "--header", "Authorization: Bearer ${API_KEY}"],
  "env": {
    "API_KEY": "${API_KEY}",
    "DOMAIN": "${DOMAIN}"
  }
}
```

### Variables in args (not just env)

Some servers pass secrets via CLI args instead of env vars. The `${VAR}` placeholder can appear in `args` entries. The variable still needs a matching `requiredSecrets` entry, and should also appear in `env` so the platform can resolve it. See `launchdarkly/` for an example where `${LAUNCHDARKLY_ACCESS_TOKEN}` is in `args`.

## requiredSecrets Conventions

Each secret entry:

```json
{
  "envVar": "SERVICE_API_KEY",        // Must match a ${VAR} in serverConfig
  "displayName": "Service API Key",   // Shown in the install dialog
  "description": "How to obtain...",  // Clear instructions
  "helpUrl": "https://..."            // Optional link to docs
}
```

**Naming conventions:**
- Use UPPER_SNAKE_CASE for `envVar`
- Prefix with the service name: `SENTRY_ACCESS_TOKEN`, `GRAFANA_URL`
- Common suffixes: `_API_KEY`, `_ACCESS_TOKEN`, `_URL`, `_TEAM_ID`, `_DOMAIN`

## recommendedTools Guidance

- Select 3-6 of the most commonly used tools
- Prefer read/query operations over write/delete operations
- Include tools that demonstrate the server's primary value
- Must be an exact subset of `allTools` — every name must match exactly
