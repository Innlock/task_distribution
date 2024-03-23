from sqlalchemy.dialects.postgresql import insert
from werkzeug.security import generate_password_hash
import random
from datetime import datetime
import json

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
            'queue_id': 3  # random.choice(queues).queue_id
        }
        a_q = insert(AssigneesQueues).values(values)
        db.session.execute(a_q)

        num_components = random.randint(1, len(components))
        random_components = random.sample(components, num_components)
        for component in random_components:
            values = {
                'assignee_id': assignee.assignee_id,
                'component_id': component.component_id
            }
            a_c = insert(AssigneesComponents).values(values)
            db.session.execute(a_c)
    db.session.commit()


def initialize_users_dummies():
    password = generate_password_hash('123', salt_length=8)
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
            queue = insert(TasksQueues).values(other_tables['queue'])
            db.session.execute(queue)
        if other_tables.get('components'):
            for component in other_tables['components']:
                comp = insert(TasksComponents).values(component)
                db.session.execute(comp)
        if other_tables.get('sprints'):
            for sprint in other_tables['sprints']:
                sp = insert(TasksSprints).values(sprint)
                db.session.execute(sp)
    db.session.commit()


def initialize_sprints_dummies():
    sprints = [
        {
            'sprint_id': 1,
            'name': 'sprint 1',
            'startDate': datetime(2024, 1, 8),
            'endDate': datetime(2024, 1, 14),
        },
        {
            'sprint_id': 2,
            'name': 'sprint 2',
            'startDate': datetime(2024, 1, 15),
            'endDate': datetime(2024, 1, 21),
        },
        {
            'sprint_id': 3,
            'name': 'sprint 3',
            'startDate': datetime(2024, 1, 22),
            'endDate': datetime(2024, 1, 28),
        },
        {
            'sprint_id': 4,
            'name': 'sprint 4',
            'startDate': datetime(2024, 1, 29),
            'endDate': datetime(2024, 2, 4),
        },
        {
            'sprint_id': 5,
            'name': 'sprint 5',
            'startDate': datetime(2024, 2, 5),
            'endDate': datetime(2024, 2, 11),
        },
    ]
    for sprint in sprints:
        spr = Sprint(**sprint)
        db.session.add(spr)
    db.session.commit()


def initialize_tasks_dummies():
    with open("./settings/tasks_dummies.json") as file:
        data = json.load(file)
        tasks = data['tasks']

    for task in tasks:
        t = Task(**task.get('task'))
        db.session.add(t)
        db.session.commit()

        queue = insert(TasksQueues).values(task.get('queue'))
        db.session.execute(queue)

        sprint = insert(TasksSprints).values(task.get('sprint'))
        db.session.execute(sprint)

        for component in task.get('components'):
            comp = insert(TasksComponents).values(component)
            db.session.execute(comp)

    db.session.commit()


def initialize_assignees_dummies():
    assignees = [
        {
            'assignee_id': '8000000000000004',
            'name': 'annachistozvonova',
            'level': 5,
            'rate': 1
        },
        {
            'assignee_id': '8000000000000005',
            'name': 'chistozvnovaam1',
            'level': 3,
            'rate': 1
        },
        {
            'assignee_id': '8000000000000006',
            'name': 'org.handsome',
            'level': 1,
            'rate': 0.5
        },
        {
            'assignee_id': '8000000000000008',
            'name': 'len.ivan2',
            'level': 3,
            'rate': 1
        },
        {
            'assignee_id': '8000000000000009',
            'name': 'yekaterina.nikitina83',
            'level': 2,
            'rate': 0.5
        },
        # {
        #     'assignee_id': '8000000000000010',
        #     'name': 'annachistozvonova',
        #     'level': 5,
        #     'rate': 1
        # },
        # {
        #     'assignee_id': '8000000000000011',
        #     'name': 'chistozvnovaam1',
        #     'level': 3,
        #     'rate': 1
        # },
        # {
        #     'assignee_id': '8000000000000012',
        #     'name': 'org.handsome',
        #     'level': 1,
        #     'rate': 0.5
        # },
        # {
        #     'assignee_id': '8000000000000013',
        #     'name': 'len.ivan2',
        #     'level': 3,
        #     'rate': 1
        # },
        # {
        #     'assignee_id': '8000000000000015',
        #     'name': 'yekaterina.nikitina83',
        #     'level': 2,
        #     'rate': 0.5
        # },
        # {
        #     'assignee_id': '8000000000000016',
        #     'name': 'chistozvnovaam1',
        #     'level': 3,
        #     'rate': 1
        # },
        # {
        #     'assignee_id': '8000000000000017',
        #     'name': 'org.handsome',
        #     'level': 1,
        #     'rate': 0.5
        # },
        # {
        #     'assignee_id': '8000000000000018',
        #     'name': 'len.ivan2',
        #     'level': 3,
        #     'rate': 1
        # },
        # {
        #     'assignee_id': '8000000000000014',
        #     'name': 'yekaterina.nikitina83',
        #     'level': 2,
        #     'rate': 0.5
        # }
    ]
    for assignee in assignees:
        a = Assignee(**assignee)
        db.session.add(a)
    db.session.commit()


def initialize_database():
    # initialize_assignees()
    initialize_assignees_dummies()
    initialize_users_dummies()

    initialize_components_from_tracker()
    initialize_queues_from_tracker()
    initialize_sprints_from_tracker()

    initialize_sprints_dummies()
    initialize_tasks_dummies()

    initialize_tasks_from_tracker('OCERED')
    initialise_assignee_connections()
