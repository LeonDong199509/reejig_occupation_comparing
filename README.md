# Reejig Occupation Skill Gap API

This project implements a data pipeline and REST API to compare skills between occupations based on the O*NET dataset. It performs ETL to load data into MySQL and exposes an API to return skill gaps between two occupations.

---

## 🚀 Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/LeonDong199509/reejig_occupation_comparing.git
cd reejig_occupation_comparing
```

### Run with Docker Compose
Build and start services from scratch (no cache):
```bash
docker compose down -v  # Optional: remove volumes
docker compose build --no-cache
docker compose up
```

### Sample Requests

Base URL: http://localhost:8000

1. Successful Skill Gap Request

Request
```
GET /skill-gap?from=41-9012.00&to=53-5031.00
```

Response (200 OK)
```
[
  "Mathematics",
  "Science",
  "Learning Strategies",
  "Instructing",
  "Equipment Selection",
  "Installation",
  "Programming",
  "Operations Monitoring",
  "Operation and Control",
  "Equipment Maintenance",
  "Troubleshooting",
  "Repairing",
  "Quality Control Analysis",
  "Systems Evaluation",
  "Management of Financial Resources",
  "Management of Material Resources"
]
```

2. No Skill Gap Found

Request
```
GET /skill-gap?from=49-2098.00&to=53-5031.00
```

Response (404 Not Found)
```
{
  "detail": "No skill gap found."
}
```

3. Missing Query Parameter

Request

GET /skill-gap?from=49-2098.00

Response (422 Unprocessable Entity)
```
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "to"],
      "msg": "Field required",
      "input": null
    }
  ]
}
```