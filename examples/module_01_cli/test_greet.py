from greet import build_greeting


def test_build_greeting_returns_a_stable_message() -> None:
    assert build_greeting("Alice") == "Hello, Alice! Welcome to Python."


def test_build_greeting_strips_extra_spaces() -> None:
    assert build_greeting("  Bob  ") == "Hello, Bob! Welcome to Python."

