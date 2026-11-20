# Design Sources Template

## Primary Source

- **Type:** Figma | Google Stitch | Local Export Folder
- **Identifier:** 
  - If Figma: URL (`https://www.figma.com/design/<fileKey>/...`), File Key
  - If Google Stitch: Project ID, Screen List
  - If Local: Local directory path (e.g. `design_export/stitch/` or `design_export/figma/`)
- **Version / Last Synced:** YYYY-MM-DD
- **Owner / Contact:** Design | Product | Client

## Additional Sources (optional)

| Name | Source Type | URL / Project ID / Path | Role | Last Synced |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |

## Pages / Screens in Scope

| Name / Page | Source Identifier (Node ID / Screen ID) | Purpose | Surface | MVP? | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Example Customer | `12:34` (Figma) / `screen_home` (Stitch) | Main Home Feed | Customer | Yes | |
| Example Components | — | Design system tokens & widgets | Shared | Yes | No direct routes |
| Example Archive | — | Outdated explorations | — | No | Ignored for graph |

## Link & Identifier Conventions

- **Figma:** Prefer links with `node-id=...` (or colon format in MCP: `12:34`).
- **Google Stitch:** Use Stitch screen names/IDs or component slugs.
- **Local:** Use relative file paths to exported screens (`design_export/screens/home.png`).

## Sync Notes

- **Extraction Method:** Figma MCP | Stitch MCP | Local Folder Walk | Manual List
- **Known Limitations:** (e.g., missing prototype transitions, partial wireframes, permissions)
