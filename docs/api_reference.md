# Launch Library 2 API Reference (SpaceX Filter)

Base URL: `https://lldev.thespacedevs.com/2.2.0`

> [!NOTE]
> All queries are automatically filtered for SpaceX using the Agency ID `121` (Launch Service Provider).

## Endpoints Used

| Endpoint             | Method | Description                    | Key Parameters          |
|----------------------|--------|--------------------------------|-------------------------|
| `/launch`            | GET    | All SpaceX launches            | `limit`, `lsp__id=121`  |
| `/launch/upcoming`   | GET    | Upcoming SpaceX launches       | `limit`, `lsp__id=121`  |
| `/launch/previous`   | GET    | Past SpaceX launches           | `limit`, `lsp__id=121`  |
| `/launch/{id}`       | GET    | Single launch details          | —                       |
| `/config/launcher`   | GET    | SpaceX rocket configurations   | `limit`, `lsp__id=121`  |
| `/config/spacecraft` | GET    | SpaceX spacecraft (capsules)   | `limit`, `lsp__id=121`  |
| `/agencies/121`      | GET    | SpaceX agency (company) info   | —                       |

## Response Format

All responses are in JSON format. Paginated endpoints return a wrapper object:
```json
{
  "count": 123,
  "next": "url",
  "previous": null,
  "results": [...]
}
```

## Authentication

No authentication is required for basic read operations on the development API.

## Error Responses

| Status Code | Meaning              |
|-------------|----------------------|
| 200         | Success              |
| 404         | Resource not found   |
| 5xx         | Server error         |

## Example Response (Launch)

```json
{
  "id": "5eb11b6b-199f-449e-9d29-6126600c0106",
  "name": "Starlink-1",
  "net": "2024-01-01T00:00:00Z",
  "status": {
    "name": "Launch Successful",
    "abbrev": "Success"
  },
  "rocket": {
    "configuration": {
      "full_name": "Falcon 9 Block 5"
    }
  },
  "pad": {
    "name": "Kennedy Space Center Complex 39A",
    "location": {
      "name": "Cape Canaveral, FL, USA"
    }
  },
  "mission": {
    "description": "Starlink constellation mission."
  }
}
```
