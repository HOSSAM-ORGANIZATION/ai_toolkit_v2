# Collaborative Socratic Problem Solving & Impact Analysis

> Non-negotiable pre-execution protocol for bugs, architecture changes, and new features.
> Forces thorough collaborative thinking and blast radius assessment before writing code.

---

## 1. Fast-Track Skip Gate (`[Skip / Quick-Fix Mode]`)

Before engaging in deep inquiry, evaluate if the task qualifies for **Fast-Track**:
- **Eligible for Fast-Track:**
  - Fixing typos, localization strings, or asset path renames.
  - Trivial single-line styling tweaks (e.g. changing token reference `p12` to `p16`).
  - Pure documentation updates.
- **Fast-Track Action:** State: `[Fast-Track: Trivial task detected. Skipping deep inquiry]` and execute immediately.
- **Ineligible (Full Protocol Required):**
  - Any bug with unknown root cause or state machine failure.
  - Any new feature, screen, or domain logic modification.
  - Any change modifying shared repositories, network interceptors, or navigation routes.

---

## 2. Socratic Probing Questions (Think With the Developer)

Before touching code, the agent must ask 2–4 targeted questions to uncover hidden edge cases:
1. **User Journey & Edge Cases:**
   - *What happens when the network drops mid-request?*
   - *What should the user see if the returned list is completely empty?*
   - *How should the UI behave if user permissions are denied?*
2. **State & Lifecycle Boundaries:**
   - *Does this screen preserve state across tab switches (AutomaticKeepAliveClientMixin)?*
   - *Is there any stream or listener that requires explicit cancellation on dispose?*
3. **Alternative Solutions:**
   - *Can we achieve this using an existing widget or use case instead of creating a new one?*

---

## 3. Impact Analysis & Blast Radius (Why & What Else?)

Nothing may be implemented without documenting the 3 Core Questions:

| Question | Evaluation Criteria |
| :--- | :--- |
| **1. Why is this solution chosen?** | Explain the technical rationale. Is it optimal or a pragmatic temporary trade-off? |
| **2. What is the Blast Radius?** | Identify every other screen, model, or route that could potentially break or regress. |
| **3. Is this the simplest suitable solution?** | Apply the **Simplicity-First Gate** (Occam’s razor). Reject premature abstractions. |

---

## 4. Execution Approval
Present the brief summary to the developer:
> "Based on our analysis, we will implement [Solution X]. Blast radius is isolated to [Module Y]. This is the simplest optimal path. Ready to proceed?"

Only proceed to code execution after developer agreement or implicit workflow approval.
