# Screen States Protocol & Proactive Scenario Proposer

> Standard specification protocol for all UI screens.
> Ensures every screen accounts for the complete state matrix and critical edge-case scenarios.

---

## 1. The Screen States Questionnaire

When authoring a screen spec or plan (`spec.md` or `plan.md`), the agent must evaluate and explicitly check the state suite:

```markdown
### Screen States Matrix: [ScreenName]
- [ ] **Initial / Uninitialized:** State before data request fires.
- [ ] **Loading / In-Flight:** Full screen shimmer skeleton or spinner.
- [ ] **Loaded / Success:** Primary content rendered with populated data.
- [ ] **Empty State:** Distinct UI when data list or entity is empty (must have an actionable CTA).
- [ ] **Failure / Error:** Themed error card or full-page fail widget with a retry button.
- [ ] **Refreshing / Pull-to-Refresh:** Background refetching while preserving existing visible content.
- [ ] **Overlay Dialogs & Sheets:** Confirmations, filters, or bottom sheets.
- [ ] **Feedback Toasts / Snackbars:** Transient feedback for user mutations.
```

---

## 2. Proactive Scenario Proposer

Developers and product managers frequently forget defensive scenarios. The AI agent must proactively evaluate and propose these 5 real-world edge cases:

### Scenario 1: Offline-First & Cache Fallback
- *Question:* Should this screen display cached local storage data when the user has no internet connection?
- *Standard Implementation:* Fetch local cache first -> render -> fetch remote -> update state seamlessly.

### Scenario 2: Network Drop & Granular Retry
- *Question:* If a network call fails, does the user lose their entered form data?
- *Standard Implementation:* Preserve input controllers in state; show a floating retry banner rather than wiping the screen.

### Scenario 3: Empty State Call-to-Action (CTA)
- *Question:* When an empty state displays (e.g. "No orders found"), what should the user do next?
- *Standard Implementation:* Never leave a dead-end. Provide a prominent button (e.g. "Browse Products" or "Add Item").

### Scenario 4: Partial Failure & Segmented Loading
- *Question:* If the header banner fails to load, should the entire product list fail?
- *Standard Implementation:* Independent async state wrappers for separate screen sections (composite state).

### Scenario 5: Session Expiry (401 Unauthorized)
- *Question:* How should this screen react if the user's auth token expires mid-action?
- *Standard Implementation:* Trigger global `unauthenticated` interceptor to show a login bottom sheet or redirect without crashing.
