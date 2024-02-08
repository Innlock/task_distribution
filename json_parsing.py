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
        'tracker_id': data["id"],
        'summary': data["summary"],
        'priority': int(data["priority"]["id"]),
    }
    return mapping

