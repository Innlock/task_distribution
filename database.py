from datetime import datetime, timedelta

from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Float, Numeric, func, desc
from api_requests import get_all_tasks
from json_parsing import get_tasks_fields
from models import *
from init import db, app
from settings.database_init import initialize_database


def get_all_assignees():
    assignees = Assignee.query.all()
    return assignees


def get_tasks_in_progress(queue_id, sprint_id=None):
    tasks = db.session.query(Task) \
        .filter((Task.status == "inProgress") & (Task.assignee_id is not None)) \
        .join(TasksQueues) \
        .filter(TasksQueues.queue_id == queue_id) \
        .join(TasksComponents)
    if sprint_id is not None:
        tasks = tasks.join(TasksSprints).filter(TasksSprints.sprint_id == sprint_id)
    return tasks.all()


def get_tasks_for_distribution(queue_id, sprint_id=None):
    tasks = db.session.query(Task) \
        .filter((Task.status == "open") & (Task.assignee_id == None)) \
        .join(TasksQueues) \
        .filter(TasksQueues.queue_id == queue_id) \
        .join(TasksComponents)
    if sprint_id is not None:
        tasks = tasks.join(TasksSprints).filter(TasksSprints.sprint_id == sprint_id)
    return tasks.order_by(desc(Task.priority)).all()


def get_all_components():
    components = Component.query.order_by(Component.component_id).all()
    return components


def get_assignee_components(assignee_id):
    components = AssigneesComponents.query.filter(AssigneesComponents.assignee_id == assignee_id).join(Component).all()
    return [component.component_id for component in components]


def get_task_components(task_id):
    components = TasksComponents.query.filter(TasksComponents.task_id == task_id).join(Component).all()
    return [component.component_id for component in components]


def find_assignee_by_id(assignee_id):
    assignee = db.session.query(Assignee).filter(Assignee.assignee_id == assignee_id).first()
    return assignee


def find_task_by_id(task_id):
    task = db.session.query(Task).filter(Task.task_id == task_id).first()
    return task


# def get_resent_tasks(queue_id):
#     resent_time = datetime.now() - timedelta(weeks=12)
#     tasks = db.session.query(Task) \
#         .filter(Task.status != "open") \
#         .join(TasksQueues) \
#         .filter(TasksQueues.queue_id == queue_id) \
#         .join(TasksSprints).join(Sprint).filter(Sprint.startDate > resent_time) \
#         .join(TasksComponents)
#     return tasks.all()


# def estimate_worktime_for_task(task):
#     task_components = db.session.query(TasksComponents).filter(TasksComponents.task_id == task.task_id).all()
#     task_components_id = list(map(lambda v: v.component_id, task_components))
#     task_priority = task.priority
#     task_complexity = task.complexity
#     # to do: оценка времени задач, если оно не указано
#     match task_complexity:
#         case 5:
#             return 'PT20H'
#         case 4:
#             return 'PT10H'
#         case 3:
#             return 'PT5H'
#         case _:
#             return 'PT2H'


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
    # from distibution import get_tasks_distribution
    # print(get_tasks_distribution(3))
