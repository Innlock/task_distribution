from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Float, Numeric
from api_requests import get_all_tasks
from json_parsing import get_tasks_fields
from models import User, Task
from init import db, app
from settings.database_init import initialize_database


def drop_all_tables():
    with app.app_context():
        db.reflect()
        db.drop_all()


def update_tasks_from_tracker(queue=None):
    count, data = get_all_tasks(queue)
    for i in range(count):
        task_params = get_tasks_fields(data[i])
        task = Task(**task_params)
        db.session.add(task)
    db.session.commit()


drop_all_tables()
init_fill_tables = False
with app.app_context():
    # проверить, существует ли таблица и выставить флаг, если нет
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        init_fill_tables = True

    # создать таблицы
    db.create_all()

    # заполнить таблицы, если они только созданы
    if init_fill_tables:
        initialize_database()
