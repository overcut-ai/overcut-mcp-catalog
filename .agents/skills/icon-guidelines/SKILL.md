---
name: Icon Guidelines
description: >
  Requirements and guidance for sourcing, preparing, and adding SVG icons
  to catalog entries. Use when adding or updating icons for MCP server entries.
---

# Icon Guidelines

Each catalog entry can include an SVG icon displayed in the Overcut MCP catalog UI.

## Requirements

- **Format:** SVG strongly preferred (PNG/WebP accepted but SVG is best)
- **Aspect ratio:** Square (1:1)
- **Minimum clarity:** Must be recognizable at 32x32px
- **Dark background:** Must render well on dark backgrounds (avoid dark-only fills without contrast)
- **File name:** `icon.svg` placed in the entry directory

## iconUrl Pattern

Always use the raw GitHub URL pointing to the file in this repo:

```
https://raw.githubusercontent.com/overcut-ai/overcut-mcp-catalog/main/{entry-dir}/icon.svg
```

The `{entry-dir}` segment must match the directory name exactly.

## Sourcing Icons

### 1. Simple Icons (preferred for well-known brands)

URL pattern: `https://cdn.simpleicons.org/{brand-slug}`

Download the SVG from [Simple Icons](https://simpleicons.org/) and save it locally. Do not use the CDN URL directly as `iconUrl` — download and commit the file.

### 2. Official press kits / brand resources

Many companies provide SVG logos in their press/brand pages:
- Look for "Press Kit", "Brand Assets", "Media Kit" on the vendor's website
- Download the icon/logo mark (not the full wordmark)

### 3. Icon libraries

- [Lucide](https://lucide.dev/) — open-source icons
- [Heroicons](https://heroicons.com/) — by Tailwind team
- Use these for generic concepts when no brand icon exists

## SVG Cleanup

Before committing an SVG:

1. **Remove metadata** — Strip `<!-- comments -->`, `<metadata>`, editor cruft
2. **Set viewBox** — Ensure `viewBox="0 0 N N"` is present (square)
3. **Single color** — For brand icons, use a single fill color or `currentColor`
4. **Remove dimensions** — Remove fixed `width`/`height` attributes; let `viewBox` control sizing
5. **Minimal markup** — Remove unnecessary `<g>` wrappers, empty attributes, `id` attributes

## Example

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF">
  <path d="M12 2L2 22h20L12 2z"/>
</svg>
```

## Checklist

- [ ] SVG file saved as `{entry-dir}/icon.svg`
- [ ] Square aspect ratio (viewBox is square)
- [ ] Recognizable at 32x32px
- [ ] Renders on dark backgrounds
- [ ] No editor metadata or comments
- [ ] `iconUrl` in catalog.json matches the raw GitHub URL pattern
