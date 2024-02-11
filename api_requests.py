import requests

head = {
    "Authorization": "OAuth y0_AgAAAABMV54jAAs_UwAAAAD6JGOqAABSxtvDxxBPVqDxjDZQ70wRhksn0A",
    "X-Cloud-Org-ID": "bpfgn4i0feoaagujdag3"
}


def get_task(task):
    session = requests.Session()
    url = f"https://api.tracker.yandex.net/v2/issues/{task}?expand=attachments"
    session.headers.update(head)
    response = session.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    return None


def get_all_tasks(get_opened=True, queue=None):
    session = requests.Session()
    url = "https://api.tracker.yandex.net/v2/issues/_search"
    filters = {
        "filter": {}
    }
    if get_opened:
        filters["filter"]["status"] = "open"
    if queue is not None:
        filters["filter"]["queue"] = queue

    session.headers.update(head)
    response = session.post(url, json=filters)
    data = response.json()
    count = response.headers.get('X-Total-Count')
    if response.status_code == 200:
        return int(count), data
    return None


def get_all_assignees():
    bots = 3
    session = requests.Session()
    url = "https://api.tracker.yandex.net/v2/users"

    session.headers.update(head)
    response = session.get(url)
    data = response.json()
    count = response.headers.get('X-Total-Count')
    if response.status_code == 200:
        return int(count)-bots, data[bots:]
    return None

