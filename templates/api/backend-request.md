# Backend API Contract Request

- **Date:** {{DATE}}
- **Feature:** {{FEATURE_NAME}}
- **Target Screens:** {{SCREENS}}
- **Status:** Pending Backend Review

---

## 1. Required Endpoint

- **Method:** `{{METHOD}}` (e.g. GET / POST / PUT / DELETE)
- **Path:** `{{API_PATH}}`
- **Authentication Required:** Yes / No (Bearer Token)

---

## 2. Request Specification

### Headers
```json
{
  "Accept": "application/json",
  "Content-Type": "application/json",
  "Accept-Language": "{{LOCALE}}"
}
```

### Query Parameters
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `page` | integer | No | Pagination page index (1-based) |
| `limit` | integer | No | Page size limit |

### Request Body (JSON)
```json
{{REQUEST_PAYLOAD_SAMPLE}}
```

---

## 3. Expected Response Specification

### HTTP 200 / 201 Success Response
```json
{{SUCCESS_PAYLOAD_SAMPLE}}
```

### Error Responses (400 / 404 / 422)
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "field_name": ["Specific error message"]
  }
}
```
