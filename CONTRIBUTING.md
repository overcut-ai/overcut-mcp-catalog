# Contributing to the Overcut MCP Catalog

Thank you for your interest in contributing! This repository is a community resource for sharing pre-configured MCP server definitions.

## Adding a New MCP Server

### 1. Create the Directory

```bash
mkdir my-server-name
```

Use `kebab-case` for the directory name (e.g., `brave-search`, `google-drive`).

### 2. Create `catalog.json`

Create a `catalog.json` file following the schema documented in [README.md](./README.md#catalog-entry-schema).

**Required fields:**
- `name` - Display name
- `description` - What the server does (1-2 sentences)
- `category` - One of: `developer-tools`, `productivity`, `data`, `monitoring`, `communication`, `ai`, `other`
- `serverConfig` - Valid MCP server configuration

**Optional but recommended:**
- `tags` - Searchable keywords
- `iconUrl` - URL to an icon (see below)
- `websiteUrl` - Link to the server's documentation or repo
- `priority` - Sort order (default: 100, lower = shown first)
- `requiredSecrets` - Secrets the user needs to provide
- `recommendedTools` - Default tools to enable
- `allTools` - Complete list of available tools

### 3. Add an Icon (Optional)

Place an icon file (preferably SVG) in the same directory as `catalog.json`. Reference it in `iconUrl` using the raw GitHub URL:

```
https://raw.githubusercontent.com/overcut-ai/overcut-mcp-catalog/main/my-server/icon.svg
```

**Icon guidelines:**
- Square aspect ratio
- Simple, recognizable design
- Works well at 32x32px
- Renders well on dark backgrounds

### 4. Validate

Ensure your `catalog.json`:
- Is valid JSON (no trailing commas)
- Has a valid `category` value
- Has `requiredSecrets` entries for every `${VAR}` in `serverConfig.env`
- Has `recommendedTools` as a subset of `allTools`

### 5. Submit a Pull Request

- Clear title: "Add [Server Name] MCP server"
- Brief description of what the server does
- Link to the upstream MCP server project if applicable

## Improving Existing Entries

- Fix incorrect tool names or descriptions
- Add missing tools to `allTools`
- Improve secret descriptions or help URLs
- Update `serverConfig` for newer package versions

## Quality Standards

- Valid JSON syntax
- Accurate tool lists (test against the actual server)
- Clear, helpful secret descriptions
- No sensitive data or credentials
- Working `serverConfig` (tested with `npx` or the relevant command)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
