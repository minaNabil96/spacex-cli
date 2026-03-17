# Launch Library 2 API Reference (SpaceX Filtered)

Base URL: `https://lldev.thespacedevs.com/2.2.0`

This project uses the Launch Library 2 (LL2) API, specifically targeting SpaceX-related data.

| Endpoint             | Method | Model Mapping | Description                   |
|----------------------|--------|---------------|-------------------------------|
| `/launch`            | GET    | `Launch`      | All SpaceX launches           |
| `/launch/upcoming`   | GET    | `Launch`      | Upcoming SpaceX launches      |
| `/launch/previous`   | GET    | `Launch`      | Past SpaceX launches          |
| `/launch/{id}`       | GET    | `Launch`      | Single launch details         |
| `/config/launcher`   | GET    | `Rocket`      | Rocket configurations         |
| `/config/spacecraft` | GET    | `Capsule`     | Spacecraft (capsule) configs  |
| `/agencies/121`      | GET    | `CompanyInfo` | SpaceX agency info            |

## Mapping Logic
- **Launches**: Mapped from LL2 `results` using `net` for date and `status` for success.
- **Rockets**: Uses `config/launcher` results.
- **Capsules**: Uses `config/spacecraft` results.
- **Company**: Mapped from Agency ID `121`.
