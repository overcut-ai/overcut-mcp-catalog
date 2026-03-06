# AGENTS.md

This file provides instructions for AI agents working with the Overcut MCP Catalog repository. It contains essential information for creating, updating, and maintaining MCP server catalog entries.

## Project Overview

This repository is the **source of truth** for the MCP Server Catalog in [Overcut](https://overcut.ai). Each directory contains a `catalog.json` that defines an MCP server — its configuration, required secrets, and available tools. Overcut fetches this catalog and presents it as a browsable gallery for one-click MCP server installation.

**Key Technologies:**

- JSON for catalog entry definitions
- SVG for server icons
- MCP (Model Context Protocol) for server communication
- npx (npm) and uvx (Python/uv) for server execution
- mcp-remote for HTTP/SSE endpoint bridging

**Detailed Reference Skills:** The `.agents/skills/` directory contains deep-dive references for catalog schema, MCP server setup, icon guidelines, and tool discovery. These are symlinked into each agent's config folder (`.claude/`, `.cursor/`, `.codex/`, `.gemini/`, `.agent/`) and activate automatically when relevant.

## Repository Structure

```
overcut-mcp-catalog/
  brave-search/
    catalog.json            # Server definition
    icon.svg                # Server icon (optional)
  sentry/
    catalog.json
    icon.svg
  ...                       # 18 entry directories total
  scripts/
    validate-catalog.py     # Validation script
  .agents/skills/
    catalog-schema/         # Schema deep-dive + field reference
    mcp-server-setup/       # Finding & configuring MCP servers
    icon-guidelines/        # SVG sourcing & requirements
    tool-discovery/         # Discovering & documenting tools
  AGENTS.md                 # This file
  CLAUDE.md                 # Points to AGENTS.md
  CONTRIBUTING.md           # Contributor guidelines
  README.md                 # Public documentation
```

## Adding New Entries

Follow this step-by-step process:

### 1. Research the MCP Server

- Find the upstream package (npm or PyPI) or HTTP endpoint
- Read its documentation for required environment variables
- Identify the available tools

### 2. Create the Directory

```bash
mkdir my-server-name
```

Use **kebab-case** for the directory name (e.g., `brave-search`, `new-relic`).

### 3. Create catalog.json

Create a `catalog.json` following the schema below. See the `catalog-schema` skill for full field details.

### 4. Add an Icon

Place an `icon.svg` in the directory. See the `icon-guidelines` skill for sourcing and requirements.

### 5. Discover Tools

Populate `allTools` with the complete tool list and select `recommendedTools`. See the `tool-discovery` skill for methods.

### 6. Validate

```bash
python3 scripts/validate-catalog.py my-server-name
```

Fix any errors before submitting.

## catalog.json Schema Quick Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Display name |
| `description` | string | Yes | 1-2 sentence summary |
| `category` | string | Yes | One of the valid categories |
| `tags` | string[] | No | Searchable keywords |
| `iconUrl` | string | No | Raw GitHub URL to icon file |
| `websiteUrl` | string | No | Link to upstream docs/repo |
| `priority` | number | No | Sort order (lower = first, default 100) |
| `serverConfig` | object | Yes | MCP server configuration |
| `requiredSecrets` | object[] | No | Secrets for installation |
| `recommendedTools` | string[] | No | Pre-selected tools (subset of allTools) |
| `allTools` | string[] | No | Complete tool list |

## Categories

| Value | Description |
|-------|-------------|
| `developer-tools` | Git, CI/CD, code analysis, feature flags |
| `productivity` | Project management, task tracking |
| `data` | Search, databases, analytics |
| `monitoring` | Error tracking, observability, APM |
| `communication` | Chat, email, notifications |
| `design` | UI/UX design tools |
| `documentation` | Knowledge bases, wikis, docs platforms |
| `incident-management` | Incident response, alerting, on-call |
| `it-service-management` | ITSM, ticketing, service desks |
| `ai` | AI/ML services, LLM tools |
| `other` | Anything that doesn't fit above |

## serverConfig Patterns

### stdio via npx (npm packages — most common)

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
  "args": ["-y", "mcp-remote", "https://api.example.com/mcp", "--header", "Authorization: Bearer ${TOKEN}"],
  "env": {
    "TOKEN": "${TOKEN}"
  }
}
```

### Variables in args

Some servers pass secrets via CLI args (e.g., LaunchDarkly). The `${VAR}` placeholder can appear in `args` entries — the platform resolves them from the user's secrets.

## Quality Standards

- Valid JSON syntax (no trailing commas, proper quoting)
- Accurate tool lists verified against the actual MCP server
- Clear, actionable secret descriptions with scopes/permissions
- No sensitive data or credentials committed
- Working `serverConfig` tested locally

## Common Patterns

**npx-based entry** (e.g., sentry, slack, brave-search): `"command": "npx"` with `-y` flag and scoped package name.

**uvx-based entry** (e.g., grafana): `"command": "uvx"` with Python package name.

**mcp-remote entry** (e.g., coralogix): Uses `npx -y mcp-remote <url>` to bridge an HTTP endpoint.

**Env var naming:** `SERVICE_API_KEY`, `SERVICE_ACCESS_TOKEN`, `SERVICE_URL` — always UPPER_SNAKE_CASE prefixed with the service name.

**Priority ranges:** 1-20 for core/popular servers, 20-50 for standard, 50-100 for niche.

**Tool naming:** Use exact names from the server — typically `snake_case` but some use `kebab-case`.

## Critical Rules

1. **Env var matching:** Every `${VAR}` in `serverConfig` (in both `env` and `args`) must have a matching `requiredSecrets` entry, and vice versa.
2. **recommendedTools subset:** Every tool in `recommendedTools` must exist in `allTools`.
3. **Kebab-case directories:** Directory names must be lowercase kebab-case.
4. **iconUrl pattern:** Must follow `https://raw.githubusercontent.com/overcut-ai/overcut-mcp-catalog/main/{dir-name}/icon.svg` — the directory segment must match the entry directory.
5. **Valid JSON:** No trailing commas, no comments, proper encoding.
6. **No secrets in code:** Never commit actual API keys, tokens, or credentials.
7. **Exact tool names:** Tool names must match what the MCP server actually exposes.
8. **Valid category:** Must be one of the 11 valid category values listed above.

## Validation Checklist

Run `python3 scripts/validate-catalog.py [entry-name]` to check:

- [ ] Directory name is kebab-case
- [ ] `catalog.json` exists and is valid JSON
- [ ] Required fields present (`name`, `description`, `category`, `serverConfig`)
- [ ] Category is in the valid set
- [ ] Every `${VAR}` in serverConfig has matching requiredSecrets (and vice versa)
- [ ] `recommendedTools` is a subset of `allTools`
- [ ] No duplicate tool names in either list
- [ ] Icon file exists if iconUrl references the repo
- [ ] iconUrl directory segment matches entry directory

## Reference Examples

**Simple** (1 secret, npx): `sentry/`, `brave-search/`

**Medium** (2 secrets, npx): `slack/` (bot token + team ID)

**Medium** (2 secrets, uvx): `grafana/` (URL + service account token)

**Complex** (mcp-remote, vars in URL): `coralogix/` (API key + domain in URL)

**Args-only vars**: `launchdarkly/` (`${VAR}` in args, empty env)

## Common Tasks

### Add a new MCP server

1. `mkdir server-name`
2. Create `catalog.json` with all fields
3. Add `icon.svg`
4. Run `python3 scripts/validate-catalog.py server-name`
5. Submit PR

### Update a tool list

1. Re-discover tools (see `tool-discovery` skill)
2. Update `allTools` in `catalog.json`
3. Check if `recommendedTools` needs changes
4. Validate

### Fix validation errors

Run the script, read the error messages, and fix the corresponding field in `catalog.json`. Common fixes:
- Add missing `requiredSecrets` entry for a `${VAR}`
- Remove a tool from `recommendedTools` that isn't in `allTools`
- Fix the category to a valid value

### Update a package version

Change the version in `serverConfig.args` (e.g., `@sentry/mcp-server@latest` to `@sentry/mcp-server@0.2.0`). Re-check tool list as tools may have changed.
