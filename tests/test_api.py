import requests


def test_skill_gap_success_e2e():
    url = "http://0.0.0.0:8000/skill-gap"
    params = {
        "from": "41-9012.00",
        "to": "53-5031.00"
    }

    response = requests.get(url, params=params)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    expected_skills = [
        "Mathematics", "Science", "Learning Strategies", "Instructing",
        "Equipment Selection", "Installation", "Programming", "Operations Monitoring",
        "Operation and Control", "Equipment Maintenance", "Troubleshooting", "Repairing",
        "Quality Control Analysis", "Systems Evaluation",
        "Management of Financial Resources", "Management of Material Resources"
    ]

    assert set(response.json()) == set(expected_skills)


def test_skill_gap_not_found_e2e():
    url = "http://0.0.0.0:8000/skill-gap"
    params = {
        "from": "49-2098.00",
        "to": "53-5031.00"
    }

    response = requests.get(url, params=params)

    assert response.status_code == 404
    assert response.json() == {"detail": "No skill gap found."}


def test_skill_gap_missing_to_param_e2e():
    url = "http://0.0.0.0:8000/skill-gap"
    params = {
        "from": "49-2098.00"
        # "to" is intentionally missing
    }

    response = requests.get(url, params=params)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "to"],
                "msg": "Field required",
                "input": None
            }
        ]
    }