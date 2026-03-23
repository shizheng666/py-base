from defaults import add_tag_safe
from references import clone_and_append


def test_clone_and_append_does_not_mutate_the_original_list() -> None:
    source = ["python", "fastapi"]

    result = clone_and_append(source, "sqlalchemy")

    assert source == ["python", "fastapi"]
    assert result == ["python", "fastapi", "sqlalchemy"]


def test_add_tag_safe_creates_a_new_list_when_tags_are_missing() -> None:
    first_call = add_tag_safe("backend")
    second_call = add_tag_safe("testing")

    assert first_call == ["backend"]
    assert second_call == ["testing"]

