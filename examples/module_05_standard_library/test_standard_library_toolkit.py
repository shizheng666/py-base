import json

from standard_library_toolkit import TaskPriority
from standard_library_toolkit import TaskRecord
from standard_library_toolkit import export_task_snapshot


def test_export_task_snapshot_creates_a_json_file(tmp_path) -> None:
    task = TaskRecord(
        title="Write docs",
        owner="Alice",
        priority=TaskPriority.HIGH,
    )

    export_path = export_task_snapshot([task], tmp_path)

    assert export_path.exists()
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["tasks"][0]["title"] == "Write docs"
    assert payload["tasks"][0]["priority"] == "high"


def test_export_task_snapshot_uses_a_unique_filename(tmp_path) -> None:
    task = TaskRecord(
        title="Write docs",
        owner="Alice",
        priority=TaskPriority.MEDIUM,
    )

    first_path = export_task_snapshot([task], tmp_path)
    second_path = export_task_snapshot([task], tmp_path)

    assert first_path != second_path
