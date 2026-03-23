import pytest

from validators import TaskPayloadError, validate_task_payload


def test_validate_task_payload_returns_normalized_data() -> None:
    payload = validate_task_payload(
        {
            "title": "  Learn FastAPI  ",
            "priority": 2,
            "due_in_days": 7,
        }
    )

    assert payload["title"] == "Learn FastAPI"
    assert payload["priority"] == 2
    assert payload["due_in_days"] == 7


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title", "  "),
        ("priority", 0),
        ("priority", 6),
        ("due_in_days", -1),
    ],
)
def test_validate_task_payload_rejects_invalid_values(field: str, value: object) -> None:
    payload = {
        "title": "Learn Python",
        "priority": 3,
        "due_in_days": 5,
    }
    payload[field] = value

    with pytest.raises(TaskPayloadError):
        validate_task_payload(payload)

