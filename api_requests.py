import requests


def get_task(task):
    session = requests.Session()
    url = f"https://api.tracker.yandex.net/v2/issues/{task}?expand=attachments"
    head = {
        "Authorization": "OAuth y0_AgAAAABMV54jAAs_UwAAAAD6JGOqAABSxtvDxxBPVqDxjDZQ70wRhksn0A",
        "X-Cloud-Org-ID": "bpfgn4i0feoaagujdag3"
    }
    session.headers.update(head)
    response = session.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    return None


def get_all_tasks():
    session = requests.Session()
    url = "https://api.tracker.yandex.net/v2/issues"
    head = {
        "Authorization": "OAuth y0_AgAAAABMV54jAAs_UwAAAAD6JGOqAABSxtvDxxBPVqDxjDZQ70wRhksn0A",
        "X-Cloud-Org-ID": "bpfgn4i0feoaagujdag3"
    }
    session.headers.update(head)
    response = session.get(url)
    data = response.json()
    count = response.headers.get('X-Total-Count')
    if response.status_code == 200:
        return int(count), data
    return None
