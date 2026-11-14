### 🧪 QA Verification Summary Card: {{FEATURE_NAME}}

- **Status:** {{STATUS_EMOJI}} **{{STATUS_LABEL}}** (Passed: {{PASSED_COUNT}}/{{TOTAL_COUNT}} checks)
- **Target Device:** {{DEVICE_PLATFORM}} ({{DEVICE_NAME}})
- **States Verified:** {{STATES_VERIFIED}}
- **RenderFlex Overflows:** {{OVERFLOW_STATUS}}

{{#HAS_FAILURES}}
#### ⚠️ Detected Failures & Blockers:
- **Failed Step:** `{{FAILED_STEP}}`
- **Error Details:** `{{ERROR_MESSAGE}}`
- **Suspected Widget / File:** `{{SUSPECTED_SOURCE}}`
- **Evidence Screenshot:** [View Snapshot]({{SCREENSHOT_PATH}})

#### 💡 Suggested Self-Healing Action:
1. {{AUTO_FIX_STEP_1}}
2. {{AUTO_FIX_STEP_2}}
{{/HAS_FAILURES}}

{{^HAS_FAILURES}}
✅ **All screen states and visual layout assertions passed.**
Ready for PR verification gate.
{{/HAS_FAILURES}}
