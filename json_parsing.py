import random


def get_tasks_fields(data=None):
    keys = [
        'id',
        'summary',
        'priority',
        'sprint',
        'tags',
        'assignee',
        'queue',
        'updatedAt',
        'status'
    ]
    if data is None:
        return keys
    mapping = {
        'task_id': data['id'],
        'key': data['key'],
        'summary': data['summary'],
        'priority': int(data['priority']['id']),
        'assignee_id': data.get('assignee', {}).get('id', None)
    }
    tables = get_task_connections(data)
    return mapping, tables


def get_task_connections(data):
    tables = {}

    if data.get('queue'):
        queue = {
            'task_id': data['id'],
            'queue_id': int(data['queue']['id']),
        }
        tables['queue'] = queue

    # if data.get('tags'):
    #     tags = data['tags']
    #     tables['tags'] = tags

    if data.get('components'):
        components = []
        for component in data['components']:
            comp = {
                'task_id': data['id'],
                'component_id': int(component['id']),
            }
            components.append(comp)
        tables['components'] = components

    if data.get('sprint'):
        sprints = []
        for sprint in data['sprint']:
            comp = {
                'task_id': data['id'],
                'sprint_id': int(sprint['id']),
            }
            sprints.append(comp)
        tables['sprints'] = sprints

    return tables


def get_assignees_fields(data):
    rate = [1, 0.5]
    mapping = {
        'assignee_id': int(data['uid']),
        'name': data['login'],
        'level': random.randint(1, 5),
        'rate': random.choice(rate),
    }
    return mapping


def get_sprints_fields(data):
    mapping = {
        'sprint_id': int(data['id']),
        'name': data['name'],
        'startDate': data['startDate'],
        'endDate': data['endDate'],
    }
    return mapping


def get_components_fields(data):
    mapping = {
        'component_id': int(data['id']),
        'name': data['name'],
    }
    return mapping


def get_queues_fields(data):
    mapping = {
        'queue_id': int(data['id']),
        'name': data['name'],  # or key
    }
    return mapping
