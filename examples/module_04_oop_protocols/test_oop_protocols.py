from oop_protocols import JsonTaskFormatter
from oop_protocols import PlainTextTaskFormatter
from oop_protocols import Task
from oop_protocols import TaskPresenter


def test_task_presenter_uses_plain_text_formatter() -> None:
    task = Task(title="Review PR", status="doing", owner="Alice")
    presenter = TaskPresenter(PlainTextTaskFormatter())

    result = presenter.present(task)

    assert result == "[doing] Review PR -> Alice"


def test_task_presenter_can_switch_to_a_different_formatter_via_protocol() -> None:
    task = Task(title="Ship API", status="done", owner="Bob")
    presenter = TaskPresenter(JsonTaskFormatter())

    result = presenter.present(task)

    assert '"title": "Ship API"' in result
    assert '"status": "done"' in result
