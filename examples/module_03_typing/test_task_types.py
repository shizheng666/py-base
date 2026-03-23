from task_types import TaskSummary, build_task_summary, status_label


def test_build_task_summary_keeps_the_core_fields() -> None:
    summary = build_task_summary(title="Ship API", status="doing", owner="Alice")

    assert summary == TaskSummary(title="Ship API", status="doing", owner="Alice")


def test_status_label_uses_match_case_for_known_statuses() -> None:
    assert status_label("todo") == "Not started"
    assert status_label("doing") == "In progress"
    assert status_label("done") == "Completed"


def test_status_label_rejects_unknown_status() -> None:
    try:
        status_label("blocked")
    except ValueError as error:
        assert "Unsupported status" in str(error)
    else:
        raise AssertionError("status_label should reject unsupported statuses")

