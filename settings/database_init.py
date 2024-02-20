from sqlalchemy.dialects.postgresql import insert
from werkzeug.security import generate_password_hash
import random

from init import db
from models import *
from api_requests import get_all_assignees, get_all_tasks, get_all_qsc
from json_parsing import *


def initialize_assignees():
    count, assignees_data = get_all_assignees()
    initialize_first_assignee(assignees_data)

    for i in range(1, count):
        assignee_data = get_assignees_fields(assignees_data[i])
        a = Assignee(**assignee_data)
        db.session.add(a)
    db.session.commit()


def initialize_first_assignee(assignees_data):
    first_assignee_data = {
        'assignee_id': assignees_data[0]['uid'],
        'name': assignees_data[0]['login'],
        'level': 5,
        'rate': 1,
    }
    a = Assignee(**first_assignee_data)
    db.session.add(a)
    db.session.commit()


def initialise_assignee_connections():
    assignees = Assignee.query.all()
    queues = Queue.query.all()
    components = Component.query.all()
    for assignee in assignees:
        values = {
            'assignee_id': assignee.assignee_id,
            'queue_id': random.choice(queues).queue_id
        }
        a_q = insert(assignee_queue).values(values)
        db.session.execute(a_q)

        num_components = random.randint(1, len(components))
        random_components = random.sample(components, num_components)
        for component in random_components:
            values = {
                'assignee_id': assignee.assignee_id,
                'component_id': component.component_id
            }
            a_c = insert(assignee_component).values(values)
            db.session.execute(a_c)
    db.session.commit()


password = generate_password_hash('123', salt_length=8)


def initialize_users():
    count, assignees_data = get_all_assignees()
    user = assignees_data[0]
    user_data = {
        'login': user['login'],
        'password': password,
        'assignee_id': '8000000000000005'
    }
    u = User(**user_data)
    db.session.add(u)
    db.session.commit()


def initialize_sprints_from_tracker():
    count, data = get_all_qsc('sprints')
    for i in range(count):
        sprints_params = get_sprints_fields(data[i])
        sprint = Sprint(**sprints_params)
        db.session.add(sprint)
    db.session.commit()


def initialize_components_from_tracker():
    count, data = get_all_qsc('components')
    for i in range(count):
        components_params = get_components_fields(data[i])
        component = Component(**components_params)
        db.session.add(component)
    db.session.commit()


def initialize_queues_from_tracker():
    count, data = get_all_qsc('queues')
    for i in range(count):
        queues_params = get_queues_fields(data[i])
        queue = Queue(**queues_params)
        db.session.add(queue)
    db.session.commit()


def initialize_tasks_from_tracker(queue=None):
    count, data = get_all_tasks(queue)
    for i in range(count):
        task_params, other_tables = get_tasks_fields(data[i])
        task = Task(**task_params)
        db.session.add(task)
        db.session.commit()

        if other_tables.get('queue'):
            queue = insert(task_queue).values(other_tables['queue'])
            db.session.execute(queue)
        if other_tables.get('components'):
            for component in other_tables['components']:
                comp = insert(task_component).values(component)
                db.session.execute(comp)
        if other_tables.get('sprints'):
            for sprint in other_tables['sprints']:
                sp = insert(task_sprint).values(sprint)
                db.session.execute(sp)
    db.session.commit()


def initialize_database():
    initialize_assignees()
    initialize_users()
    initialize_components_from_tracker()
    initialize_queues_from_tracker()
    initialize_sprints_from_tracker()
    initialize_tasks_from_tracker()
    initialise_assignee_connections()
