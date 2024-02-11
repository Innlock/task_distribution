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
    #  Мб понадобятся: 'key'
    if data is None:
        return keys
    mapping = {
        'task_id': data["id"],
        'summary': data["summary"],
        'priority': int(data["priority"]["id"]),
        'assignee_id': data.get("assignee", {}).get("id", None)
    }
    return mapping


def get_assignees_fields(data):
    rate = [1, 0.5]
    mapping = {
        'assignee_id': int(data["uid"]),
        'name': data["login"],
        'level': random.randint(1, 5),
        'rate': random.choice(rate),
    }
    return mapping
