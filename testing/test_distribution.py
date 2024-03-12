import pytest

from database import *
from distribution import *

assignees_template_1 = [
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
assignees_template_2 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 5,
        'rate': 0
    }
]
assignees_template_3 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 1,
        'rate': 1
    },
    {
        'assignee_id': '2',
        'name': 'assignee2',
        'level': 1,
        'rate': 0.5
    }
]
assignees_template_4 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 1,
        'rate': 1
    },
    {
        'assignee_id': '2',
        'name': 'assignee2',
        'level': 2,
        'rate': 1
    }
]
assignees_template_5 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 1,
        'rate': 1
    },
    {
        'assignee_id': '2',
        'name': 'assignee2',
        'level': 2,
        'rate': 0.5
    }
]
assignees_template_6 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 1,
        'rate': 1
    },
    {
        'assignee_id': '2',
        'name': 'assignee2',
        'level': 1,
        'rate': 1
    }
]
assignees_template_7 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 5,
        'rate': 0.09
    }
]
assignees_template_8 = [
    {
        'assignee_id': '1',
        'name': 'assignee1',
        'level': 5,
        'rate': 1
    }
]

tasks_template_1 = [
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
    },
    {
        "task_id": "dummy-6",
        "key": "dummy-6",
        "summary": "dummy-6",
        "priority": 2,
        "complexity": 2,
        "status": "inProgress",
        "assignee_id": "3",
        "estimation": "PT4H"
    },
]
tasks_template_2 = [
    {
        "task_id": "dummy-1",
        "key": "dummy-1",
        "summary": "dummy-1",
        "priority": 2,
        "complexity": 2,
        "status": "open",
        "estimation": "PT4H"
    },
]
tasks_template_3 = [
    {
        "task_id": "dummy-1",
        "key": "dummy-1",
        "summary": "dummy-1",
        "priority": 2,
        "complexity": 2,
        "status": "open",
        "estimation": "PT4H"
    },
    {
        "task_id": "dummy-2",
        "key": "dummy-2",
        "summary": "dummy-2",
        "priority": 2,
        "complexity": 2,
        "status": "open",
        "estimation": "PT4H"
    },
]

distribution_0 = {
    'NotAssigned': [],
}
distribution_1 = {
    'NotAssigned': [],
    Assignee(**assignees_template_1[0]).assignee_id: [],
    Assignee(**assignees_template_1[1]).assignee_id: [],
    Assignee(**assignees_template_1[2]).assignee_id: [],
}
distribution_2 = {
    'NotAssigned': [Task(**tasks_template_1[0]).task_id, Task(**tasks_template_1[5]).task_id],
    Assignee(**assignees_template_1[0]).assignee_id: [Task(**tasks_template_1[1]).task_id],
    Assignee(**assignees_template_1[1]).assignee_id: [Task(**tasks_template_1[2]).task_id,
                                                      Task(**tasks_template_1[3]).task_id],
    Assignee(**assignees_template_1[2]).assignee_id: [],
}
distribution_3 = {
    'NotAssigned': [Task(**tasks_template_2[0]).task_id],
    Assignee(**assignees_template_2[0]).assignee_id: [],
}
distribution_4 = {
    'NotAssigned': [],
    Assignee(**assignees_template_3[0]).assignee_id: [Task(**tasks_template_2[0]).task_id],
    Assignee(**assignees_template_3[1]).assignee_id: [],
}
distribution_5 = {
    'NotAssigned': [],
    Assignee(**assignees_template_4[0]).assignee_id: [],
    Assignee(**assignees_template_4[1]).assignee_id: [Task(**tasks_template_2[0]).task_id],
}
distribution_6 = {
    'NotAssigned': [],
    Assignee(**assignees_template_5[0]).assignee_id: [Task(**tasks_template_3[0]).task_id],
    Assignee(**assignees_template_5[1]).assignee_id: [Task(**tasks_template_3[1]).task_id],
}
distribution_7 = {
    'NotAssigned': [],
    Assignee(**assignees_template_5[0]).assignee_id: [Task(**tasks_template_2[0]).task_id],
}

components_1 = [
    {
        "component_id": 1
    }
]
components_2 = [
    {
        "component_id": 1
    },
    {
        "component_id": 2
    }
]

tasks_components_1 = {
    'dummy-1': [1]
}

assignees_components_1 = {
    '1': [1],
    '2': [2]
}
assignees_components_2 = {
    '1': [2]
}


def transform_result_distribution(result_distribution, distribution_template):
    result = {"NotAssigned": [task.task_id for task in result_distribution.get("NotAssigned")]}
    del distribution_template["NotAssigned"]
    for assignee, tasks in distribution_template.items():
        if tasks:
            result[assignee.assignee_id] = [task.task_id for task in tasks]
        else:
            result[assignee.assignee_id] = []
    return result


@pytest.mark.parametrize("assignees_template,tasks_template,distribution",
                         [
                             # Пустые очереди
                             ([], [], distribution_0),
                             # Нет задач
                             (assignees_template_1, [], distribution_1),
                             # Сотрудник не доступен, 1 задача для 1 сотрудника,
                             # 2 задачи для 1, задача без исполнителя, задача без оценки
                             (assignees_template_1, tasks_template_1, distribution_2)
                         ])
def test_fill_tasks_in_progress(assignees_template, tasks_template, distribution):
    assignees = []
    tasks = []
    for assignee in assignees_template:
        assignees.append(Assignee(**assignee))
    for task in tasks_template:
        tasks.append(Task(**task))
    distribution_template = create_template(assignees)
    worktime = get_assignees_worktime(assignees)

    result_distribution = fill_tasks_in_progress(tasks, distribution_template, worktime, assignees)
    result = transform_result_distribution(result_distribution, distribution_template)
    assert result == distribution


@pytest.mark.parametrize("assignees_template,tasks_template,all_components,distribution",
                         [
                             # Пустые очереди - нет
                             ([], [], ([], {}, {}), distribution_0),
                             # Сотрудник не доступен, задача есть - нет
                             (assignees_template_2, tasks_template_2, (components_1, {}, {}), distribution_3),
                             # Есть 2 сотрудника, у одного больше рабочего времени - время
                             (assignees_template_3, tasks_template_2, (components_1, {}, {}), distribution_4),
                             # Есть 2 сотрудника, у одного более подходящий уровень - уровень
                             (assignees_template_4, tasks_template_2, (components_1, {}, {}), distribution_5),
                             # Есть 2 сотрудника, у одного более подходящий уровень, у другого больше времени - уровень
                             (assignees_template_5, tasks_template_2, (components_1, {}, {}), distribution_5),
                             # 2 одинаковых сотрудника, 2 одинаковых задачи - поровну
                             (assignees_template_6, tasks_template_3, (components_1, {}, {}), distribution_6),
                             # У сотрудника не хватает времени на задачу - нет
                             (assignees_template_7, tasks_template_2, (components_1, {}, {}), distribution_3),
                             # 2 сотрудника с разными компетенциями, 1 задача - по компетенции
                             (assignees_template_6, tasks_template_2,
                              (components_2, tasks_components_1, assignees_components_1), distribution_4),
                             # Есть 2 сотрудника, у 2 более подходящий уровень, у 1 компетенции - по компетенции
                             (assignees_template_4, tasks_template_2,
                              (components_2, tasks_components_1, assignees_components_1), distribution_4),
                             # Сотрудник 1, задача вне компетенций и уровня - задача назначается
                             (assignees_template_8, tasks_template_2,
                              (components_2, tasks_components_1, assignees_components_2), distribution_7),
                         ])
def test_distribute_open_tasks(assignees_template, tasks_template, all_components, distribution):
    components_template, tasks_components, assignees_components = all_components
    assignees = []
    tasks_for_distribution = []
    components = []

    for component in components_template:
        components.append(Component(**component))
    for assignee in assignees_template:
        assignees.append(Assignee(**assignee))
    for task in tasks_template:
        tasks_for_distribution.append(Task(**task))

    distribution_template = create_template(assignees)
    worktime = get_assignees_worktime(assignees)

    all_components = components, tasks_components, assignees_components
    assignee_info = assignees, worktime, tasks_for_distribution

    result_distribution = distribute_open_tasks(all_components, distribution_template, assignee_info)
    result = transform_result_distribution(result_distribution, distribution_template)
    assert result == distribution
