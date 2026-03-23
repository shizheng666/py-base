from sqlalchemy_tasks import TaskCreate
from sqlalchemy_tasks import create_task
from sqlalchemy_tasks import list_tasks
from sqlalchemy_tasks import make_session


def test_create_task_persists_one_row() -> None:
    session = make_session()

    task = create_task(
        session,
        TaskCreate(title="Learn SQLAlchemy", priority=2),
    )

    assert task.id == 1
    assert task.title == "Learn SQLAlchemy"


def test_list_tasks_returns_rows_in_creation_order() -> None:
    session = make_session()
    create_task(session, TaskCreate(title="First task", priority=1))
    create_task(session, TaskCreate(title="Second task", priority=3))

    tasks = list_tasks(session)

    assert [task.title for task in tasks] == ["First task", "Second task"]
