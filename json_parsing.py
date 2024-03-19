import random
import isodate
from datetime import timedelta


def parse_work_time_to_normal_time(work_days):
    if work_days is None:
        return None
    work_days = isodate.parse_duration(work_days)
    normal_days = work_days.days
    if work_days.days > 6:
        normal_days = work_days.days // 7 * 5 + work_days.days % 7

    normal_hours = work_days - timedelta(days=work_days.days)
    days_to_hours = timedelta(hours=normal_days * 8)
    normal_time = normal_hours + days_to_hours
    return isodate.duration_isoformat(normal_time)


def parse_normal_time_to_work_time(normal_days):
    if normal_days is None:
        return None
    normal_days = isodate.parse_duration(normal_days)
    normal_hours = normal_days.seconds // 3600 + normal_days.days * 24
    work_seconds = normal_days.seconds % 3600
    work_days = normal_hours // 8
    work_hours = normal_hours % 8
    if work_days > 4:
        work_days = work_days // 5 * 7 + work_days % 5
    work_time = timedelta(days=work_days, hours=work_hours, seconds=work_seconds)
    return isodate.duration_isoformat(work_time)


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
        'complexity': int(data['storyPoints']),
        'status': data['status']['key'],
        'estimation': parse_work_time_to_normal_time(data.get('estimation', None)),
        # 'time_spent': parse_work_time_to_normal_time(data.get('spent', None)),
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
            spr = {
                'task_id': data['id'],
                'sprint_id': int(sprint['id']),
            }
            sprints.append(spr)
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
