from unittest.mock import patch

from database import *
from distribution import *

assignees_template = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 3,
        'rate': 1
    },
    {
        'assignee_id': '2',
        'name': 'assignee2',
        'level': 4,
        'rate': 0.5
    },
    {
        'assignee_id': '3',
        'name': 'assignee3',
        'level': 5,
        'rate': 0
    }
]


def test_fill_tasks_in_progress_empy():
    assignees = []
    tasks = []
    for assignee in assignees_template:
        assignees.append(Assignee(**assignee))

    distribution_template = create_template(assignees)
    worktime = get_assignees_worktime(assignees)

    result = fill_tasks_in_progress(tasks, distribution_template, worktime, assignees)
    distribution = {
        'NotAssigned': [],
        assignees[0]: [],
        assignees[1]: [],
        assignees[2]: [],
    }
    assert result == distribution


def test_fill_tasks_in_progress():
    tasks_template = [
        {
            "task_id": "dummy-1",
            "key": "dummy-1",
            "summary": "dummy-1",
            "priority": 2,
            "complexity": 2,
            "status": "inProgress",
            "estimation": "PT4H"
        },
        {
            "task_id": "dummy-2",
            "key": "dummy-2",
            "summary": "dummy-2",
            "priority": 2,
            "complexity": 2,
            "status": "inProgress",
            "estimation": "PT4H",
            "assignee_id": "1"
        },
        {
            "task_id": "dummy-3",
            "key": "dummy-3",
            "summary": "dummy-3",
            "priority": 2,
            "complexity": 2,
            "status": "inProgress",
            "estimation": "PT4H",
            "assignee_id": "2"
        },
        {
            "task_id": "dummy-4",
            "key": "dummy-4",
            "summary": "dummy-4",
            "priority": 2,
            "complexity": 2,
            "status": "inProgress",
            "estimation": "PT4H",
            "assignee_id": "2"
        },
        {
            "task_id": "dummy-5",
            "key": "dummy-5",
            "summary": "dummy-5",
            "priority": 2,
            "complexity": 2,
            "status": "inProgress",
            "assignee_id": "2"
        }
    ]
    assignees = []
    tasks = []
    for assignee in assignees_template:
        assignees.append(Assignee(**assignee))
    for task in tasks_template:
        tasks.append(Task(**task))
    distribution_template = create_template(assignees)
    worktime = get_assignees_worktime(assignees)

    result = fill_tasks_in_progress(tasks, distribution_template, worktime, assignees)
    distribution = {
        'NotAssigned': [],
        assignees[0]: [tasks[1]],
        assignees[1]: [tasks[2], tasks[3]],
        assignees[2]: [],
    }
    assert result == distribution


def test_distribute_open_tasks_empty():
    pass


def test_distribute_open_tasks():
    pass
