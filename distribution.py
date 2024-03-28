import math
import isodate
from datetime import timedelta

from database import *


def create_template(assignees):
    distribution = {
        'NotAssigned': []
    }
    for assignee in assignees:
        distribution[assignee] = []
    return distribution


def get_assignees_worktime(assignees):
    worktime = {}
    for assignee in assignees:
        worktime[assignee.assignee_id] = timedelta(hours=int(assignee.rate * 40))
    return worktime


def fill_tasks_in_progress(tasks_in_progress, distribution, worktime, assignees):
    if not assignees:
        return distribution
    for task in tasks_in_progress:
        if not task.estimation:
            continue
        estimation = isodate.parse_duration(task.estimation)
        if task.assignee_id and worktime[task.assignee_id] >= estimation:
            assignee = assignee_by_id(task.assignee_id, assignees)
            if assignee:
                distribution[assignee].append(task)
                worktime.update(
                    {task.assignee_id: worktime[task.assignee_id] - estimation})
        else:
            distribution['NotAssigned'].append(task)
    return distribution


def assignee_by_id(assignee_id, assignees):
    for assignee in assignees:
        if assignee.assignee_id == assignee_id:
            return assignee
    return None


def get_assignees_vector_dir(assignees, components, assignees_components):
    vector_dir = {}
    for assignee in assignees:
        assignee_components = assignees_components.get(assignee.assignee_id)
        assignee_components_vectors = get_at_components_vector(assignee_components, components)

        vector = (assignee.level, *assignee_components_vectors)
        if vector_dir.get(vector):
            vector_dir[vector].append(assignee.assignee_id)
        else:
            vector_dir[vector] = [assignee.assignee_id]
    return vector_dir


def get_at_components_vector(at_components, components):
    if not at_components:
        at_components = []
    components_vectors = []
    for component in components:
        if component.component_id in at_components:
            components_vectors.append(5)
        else:
            components_vectors.append(0)
    return components_vectors


def get_most_similar_vector(task, vectors_list, assignees_vector_dir):
    min_distance = None
    most_similar_vector = None
    for assignee_vector in vectors_list:
        distance = math.sqrt(sum([(p1 - p2) ** 2 for p1, p2 in zip(assignee_vector, task)]))
        if most_similar_vector is None or distance <= min_distance:
            min_distance = distance
            most_similar_vector = assignee_vector

    assignees = assignees_vector_dir.get(most_similar_vector)
    return assignees


def get_available_assignees(estimation, assignees_vector_dir, assignees_work_time):
    available_assignees = []
    for assignee_id, worktime in assignees_work_time.items():
        if worktime >= estimation:
            for assignee_vector, assignees_id in assignees_vector_dir.items():
                if assignee_id in assignees_id:
                    available_assignees.append(assignee_vector)
    return available_assignees


def get_available_assignee(estimation, assignees_id, assignees_work_time, assignees):
    assignee_id = assignees_id[0]
    if len(assignees_id) == 1:
        return assignee_by_id(assignee_id, assignees)

    assignees_ids = []
    for assign_id, worktime in assignees_work_time.items():
        if assign_id in assignees_id and worktime >= estimation:
            assignees_ids.append(assign_id)
    assignee_id = get_assignee_with_more_worktime(assignees_ids, assignees_work_time)
    return assignee_by_id(assignee_id, assignees)


def get_assignee_with_more_worktime(assignees, assignees_work_time):
    if not assignees:
        return None
    assignee_with_more_worktime = assignees[0]
    worktime = assignees_work_time[assignee_with_more_worktime]
    for assignee in assignees:
        if assignees_work_time[assignee] > worktime:
            assignee_with_more_worktime = assignee
            worktime = assignees_work_time[assignee]
    return assignee_with_more_worktime


def distribute_open_tasks(all_components, distribution, assignee_info):
    assignees, assignees_work_time, tasks_for_distribution = assignee_info
    components, tasks_components, assignees_components = all_components
    if not assignees or not tasks_for_distribution:
        return distribution

    assignees_vector_dir = get_assignees_vector_dir(assignees, components, assignees_components)

    for task in tasks_for_distribution:
        if not task.estimation:
            continue

        task_components = tasks_components.get(task.task_id)
        task_components_vectors = get_at_components_vector(task_components, components)

        vector = (task.complexity, *task_components_vectors)

        estimation = isodate.parse_duration(task.estimation)
        available_assignees = get_available_assignees(estimation, assignees_vector_dir, assignees_work_time)
        if len(available_assignees) == 0:
            distribution['NotAssigned'].append(task)
            continue
        assignees_id = get_most_similar_vector(vector, available_assignees, assignees_vector_dir)
        assignee = get_available_assignee(estimation, assignees_id, assignees_work_time, assignees)

        assignees_work_time.update(
            {assignee.assignee_id: assignees_work_time[assignee.assignee_id] - estimation})
        distribution[assignee].append(task)
    return distribution


def get_tasks_distribution(user_id, queue_id, sprint_id=None):
    # Перенести не законченные задачи
    assignees = get_all_assignees()
    distribution = create_template(assignees)
    assignees_work_time = get_assignees_worktime(assignees)

    tasks_in_progress = get_tasks_in_progress(queue_id)
    distribution = fill_tasks_in_progress(tasks_in_progress, distribution, assignees_work_time, assignees)

    # Распределить остальные задачи
    tasks_for_distribution = get_tasks_for_distribution(queue_id, sprint_id)
    components = get_all_components()

    tasks_components = {}
    for task in tasks_for_distribution:
        tasks_components[task.task_id] = get_task_components(task.task_id)

    assignees_components = {}
    for assignee in assignees:
        assignees_components[assignee.assignee_id] = get_assignee_components(assignee.assignee_id)

    all_components = components, tasks_components, assignees_components
    assignee_info = assignees, assignees_work_time, tasks_for_distribution

    distribution = distribute_open_tasks(all_components, distribution, assignee_info)
    temp_save_distribution(distribution, user_id, queue_id, sprint_id)
    return distribution
