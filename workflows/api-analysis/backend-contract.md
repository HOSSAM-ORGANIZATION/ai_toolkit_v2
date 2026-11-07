# Backend Contract Kit: Collaboration Protocol

> Formalized protocol for communicating API requirements, discrepancies, and schema agreements with backend teams.

---

## 1. The 4 Contract Actions

### 1. Request (`backend-contract request`)
When a Flutter screen requires endpoints or fields that are missing or mismatched in the API collection:
1. Create `ai_specs/api/contracts/pending/<date>-<feature>-request.md` using `templates/api/backend-request.md`.
2. Specify exact endpoint, method, expected payload, headers, and query parameters.
3. Include real sample JSON responses matching the UI requirement.

### 2. Check (`backend-contract check`)
Check status of pending contract requests against agreed replies in `ai_specs/api/contracts/agreed/`.

### 3. Intake (`backend-contract intake`)
When the backend team replies:
1. Move request to `ai_specs/api/contracts/agreed/<date>-<feature>-reply.md`.
2. Record field mappings or backend deviations.

### 4. Apply (`backend-contract apply`)
Update Flutter DTOs (`models/`), datasources, and repositories to match the agreed contract.
