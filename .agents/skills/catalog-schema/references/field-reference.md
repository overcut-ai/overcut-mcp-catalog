# Exhaustive Field Reference

## name (required)
- **Type:** string
- **Constraints:** Non-empty. Should match the official product name.
- **Examples:** `"Sentry"`, `"Brave Search"`, `"LaunchDarkly"`

## description (required)
- **Type:** string
- **Constraints:** 1-2 sentences. Describe what the MCP server enables.
- **Style:** Start with a verb. Focus on capabilities, not marketing.
- **Examples:**
  - `"Search errors, investigate issues, and access Seer AI root-cause analysis from Sentry."`
  - `"Send messages, read channels, and interact with your Slack workspace."`

## category (required)
- **Type:** string enum
- **Valid values:** `developer-tools`, `productivity`, `data`, `monitoring`, `communication`, `design`, `documentation`, `incident-management`, `it-service-management`, `ai`, `other`
- **Constraints:** Must be exactly one of the valid values. No custom categories.

## tags (optional)
- **Type:** string[]
- **Constraints:** Lowercase kebab-case. 3-6 tags recommended.
- **Purpose:** Searchable keywords for catalog discovery.
- **Examples:** `["errors", "debugging", "observability"]`

## iconUrl (optional)
- **Type:** string (URL)
- **Pattern:** `https://raw.githubusercontent.com/overcut-ai/overcut-mcp-catalog/main/{dir-name}/icon.svg`
- **Constraints:** Must reference a file that exists in the repo. Directory segment must match entry directory name.

## websiteUrl (optional)
- **Type:** string (URL)
- **Purpose:** Link to the upstream MCP server project, docs, or homepage.
- **Examples:** GitHub repo URL, official docs page.

## priority (optional)
- **Type:** number
- **Default:** 100
- **Constraints:** Lower = shown first. Use 1-20 for core/popular servers, 20-50 for standard, 50-100 for niche.
- **Examples:** Sentry/Grafana = 10, Slack = 20, Brave Search = 30

## serverConfig (required)
- **Type:** object
- **Purpose:** The actual MCP server configuration passed to the MCP client.

### serverConfig.command (required for stdio)
- **Type:** string
- **Values:** `"npx"` (npm packages), `"uvx"` (Python packages), or a custom command.

### serverConfig.args (required for stdio)
- **Type:** string[]
- **npx pattern:** `["-y", "@scope/package@latest"]` or `["-y", "package-name"]`
- **uvx pattern:** `["package-name"]`
- **mcp-remote pattern:** `["-y", "mcp-remote", "<url>", "--header", "Authorization: Bearer ${VAR}"]`
- May contain `${VAR}` placeholders that get resolved from secrets.

### serverConfig.env (optional)
- **Type:** object (string -> string)
- **Purpose:** Environment variables passed to the server process.
- **Values:** Use `"${VAR_NAME}"` for secret placeholders, or literal values.
- Can be an empty object `{}` if all vars are passed via args.

## requiredSecrets (optional)
- **Type:** object[]
- **Purpose:** Defines secrets the user must provide during installation.

### requiredSecrets[].envVar (required)
- **Type:** string
- **Constraints:** UPPER_SNAKE_CASE. Must match a `${VAR}` in serverConfig (in env or args).

### requiredSecrets[].displayName (required)
- **Type:** string
- **Purpose:** Human-readable label shown in the install dialog.

### requiredSecrets[].description (required)
- **Type:** string
- **Purpose:** Instructions for obtaining the secret. Be specific about scopes, permissions, and where to find it.

### requiredSecrets[].helpUrl (optional)
- **Type:** string (URL)
- **Purpose:** Direct link to documentation for creating the secret.

## recommendedTools (optional)
- **Type:** string[]
- **Constraints:** Every entry must exist in `allTools`. Typically 3-6 tools.
- **Purpose:** Tools pre-selected when the user installs the server.

## allTools (optional)
- **Type:** string[]
- **Constraints:** No duplicates. Names must match the exact tool names exposed by the MCP server.
- **Purpose:** Complete list of tools the server provides. Users can toggle these on/off.
