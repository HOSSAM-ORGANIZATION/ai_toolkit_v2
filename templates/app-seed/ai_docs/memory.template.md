# App Memory & Architecture Gotchas

> Living document (<= 4 KB).
> Captures cross-cutting gotchas, lessons learned, and third-party quirks.
> Rule: Replace rows when updating; do not allow unbounded growth.

## 1. Quick Technical Constraints
| Key | Value |
| :--- | :--- |
| **Project Name** | `{{PROJECT_NAME}}` |
| **Archetype** | `{{PROJECT_TYPE}}` |
| **Active Flavors** | `{{FLAVORS_LIST}}` |
| **Design Source** | `{{DESIGN_SOURCE}}` |
| **Testing Gate** | `{{TESTING_GATE}}` |

## 2. Shared Component Registry
| Component | Implementation | Notes / Constraints |
| :--- | :--- | :--- |
| Primary Button | `{{TOKEN_BUTTON_NAME}}` | Handles async loading spinner automatically |
| Back Affordance | `{{TOKEN_BACK_BUTTON_NAME}}` | Auto-mirrored for RTL; don't use raw back icons |
| Image Loader | `{{TOKEN_IMAGE_NAME}}` | CachedNetworkImage with Shimmer placeholder |

## 3. Known Gotchas & Lessons Learned
| Area / Package | Quirk or Gotcha | Approved Solution / Workaround |
| :--- | :--- | :--- |
| *e.g. VideoPlayer* | *Fails on iOS without file caching* | *Pre-cache remote URL to local temp file first* |
| *e.g. SVG Icons* | *ColorFilter deprecation* | *Use ColorFilter.mode(color, BlendMode.srcIn)* |
