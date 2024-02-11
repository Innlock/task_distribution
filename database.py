from api_requests import get_all_tasks
from json_parsing import get_tasks_fields
from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Float, Numeric
from models import User, Task
from init import db, app
from settings.database_users_init import initialize_assignees, initialize_users



def drop_all_tables():
    with app.app_context():
        db.reflect()
        db.drop_all()


def update_tasks_from_tracker():
    count, data = get_all_tasks()
    for i in range(count):
        task_params = get_tasks_fields(data[i])
        task = Task(**task_params)
        db.session.add(task)
        # print(data[i].get("assignee"))
    db.session.commit()



drop_all_tables()
fill_tables = False
with app.app_context():
    # проверить, существует ли таблица и выставить флаг, если нет
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        fill_tables = True

    # создать таблицы
    db.create_all()

    # заполнить таблицы, если они только созданы
    if fill_tables:
        initialize_assignees()
        initialize_users()
        update_tasks_from_tracker()
