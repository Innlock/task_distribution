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


def get_tasks_in_progress(queue_id):
    tasks = db.session.query(Task) \
        .filter((Task.status == "inProgress") & (Task.assignee_id is not None)) \
        .join(TasksQueues) \
        .filter(TasksQueues.queue_id == queue_id) \
        .join(TasksComponents)
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
    print("Dropping all tables...")
    with app.app_context():
        db.reflect()
        db.drop_all()


def drop_all_tables_but_users():
    AssigneesTasksTemp.query.delete()
    Assignment.query.delete()

    AssigneesComponents.query.delete()
    AssigneesQueues.query.delete()

    TasksComponents.query.delete()
    TasksSprints.query.delete()
    TasksQueues.query.delete()

    Task.query.delete()
    User.query.filter(User.assignee_id != None).update({'assignee_id': None})
    Assignee.query.delete()

    Sprint.query.delete()
    Component.query.delete()
    Queue.query.delete()
    db.session.commit()
    print("Dropping some tables...")


def update_tasks_from_tracker(queue=None):
    count, data = get_all_tasks(queue)
    for i in range(count):
        task_params = get_tasks_fields(data[i])
        task = Task(**task_params)
        db.session.add(task)
    db.session.commit()


def login_in_assignees(username):
    assignee = db.session.query(Assignee).filter(Assignee.name == username).first()
    if assignee is None:
        return False
    return True


def get_all_queues():
    queues = Queue.query.all()
    return queues


def get_all_sprints():
    sprints = Sprint.query.all()
    return sprints


def temp_save_distribution(distribution, user_id, queue_id, sprint_id):
    auto_name = "auto_generated"
    Assignment.query.filter_by(user_id=user_id, queue_id=queue_id, sprint_id=sprint_id,
                               name=auto_name).delete()

    if sprint_id is None:
        assignment = Assignment(user_id=user_id, queue_id=queue_id, name=auto_name)
    else:
        assignment = Assignment(user_id=user_id, queue_id=queue_id, name=auto_name, sprint_id=sprint_id)
    db.session.add(assignment)
    db.session.commit()
    for assignee, tasks in distribution.items():
        for task in tasks:
            temp_dist = AssigneesTasksTemp(task_id=task.task_id, assignee_id=assignee.assignee_id,
                                           assignment_id=assignment.assignment_id)
            db.session.add(temp_dist)
    db.session.commit()


# Пока обновляется вся БД
def sync_data_in_database(completely=True, assignee_id=None):
    if completely:
        drop_all_tables()
    else:
        drop_all_tables_but_users()

    init_fill_tables = False
    with app.app_context():
        # проверить, существует ли таблица и выставить флаг, если нет
        inspector = inspect(db.engine)
        if "users" not in inspector.get_table_names() or not completely:
            init_fill_tables = True

        # создать таблицы
        db.create_all()

        # заполнить таблицы, если они только созданы
        if init_fill_tables:
            initialize_database(completely)


def create_template(assignees):
    distribution = {
        'NotAssigned': []
    }
    for assignee in assignees:
        distribution[assignee] = []
    return distribution


def get_auto_distribution(user_id, queue_id, sprint_id):
    auto_name = "auto_generated"
    assignees = Assignee.query.all()
    distribution = create_template(assignees)

    assignment = Assignment.query.filter(
        Assignment.user_id == user_id,
        Assignment.queue_id == queue_id,
        Assignment.sprint_id == sprint_id,
        Assignment.name == auto_name
    ).first()

    if assignment is None:
        print("No assignment found")
        return None
    assignee_tasks = AssigneesTasksTemp.query.filter_by(assignment_id=assignment.assignment_id).all()
    assignee_ids = [row.assignee_id for row in assignee_tasks]
    task_ids = [row.task_id for row in assignee_tasks]

    assignees_obj = Assignee.query.filter(Assignee.assignee_id.in_(assignee_ids)).all()
    assignees = {assignee.assignee_id: assignee for assignee in assignees_obj}

    tasks_obj = Task.query.filter(Task.task_id.in_(task_ids)).all()
    tasks = {task.task_id: task for task in tasks_obj}

    for assign in assignee_tasks:
        distribution[assignees.get(assign.assignee_id)].append(tasks.get(assign.task_id))
    print(distribution)
    return distribution


sync_data_in_database()
