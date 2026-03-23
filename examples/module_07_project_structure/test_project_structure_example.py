from project_structure_example import FeaturePlan
from project_structure_example import build_task_feature_plan
from project_structure_example import quality_commands


def test_build_task_feature_plan_assigns_clear_responsibilities() -> None:
    plan = build_task_feature_plan()

    assert isinstance(plan, FeaturePlan)
    assert "schemas.py" in plan.files_by_role["input_output"]
    assert "services.py" in plan.files_by_role["business_logic"]
    assert "routes.py" in plan.files_by_role["http_entry"]


def test_quality_commands_list_the_expected_checks() -> None:
    commands = quality_commands()

    assert "uv run pytest -q" in commands
    assert "uv run ruff check ." in commands
    assert "uv run mypy ." in commands
