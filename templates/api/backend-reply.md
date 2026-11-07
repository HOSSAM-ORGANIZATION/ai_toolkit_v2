# Backend API Contract Reply & Agreement

- **Date:** {{DATE}}
- **Feature:** {{FEATURE_NAME}}
- **Status:** Agreed & Locked

---

## 1. Agreed Endpoint & Mapping
- **Agreed Path:** `{{AGREED_PATH}}`
- **Agreed Method:** `{{METHOD}}`

---

## 2. Agreed Response Envelope
```json
{{AGREED_JSON_SAMPLE}}
```

---

## 3. Deviations & Field Renames
| Mobile Requested Field | Backend Agreed Key | Type / Notes |
| :--- | :--- | :--- |
| `is_verified` | `email_verified_at` | Non-null timestamp indicates true |
| `image_url` | `avatar` | Absolute URL string |

---

## 4. Mobile Action Items
- [ ] Update `models/` from `fromAgreedJson`
- [ ] Update remote datasource endpoint path
- [ ] Verify test mock matches agreed payload
