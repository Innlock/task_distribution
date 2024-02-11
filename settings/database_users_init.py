from werkzeug.security import generate_password_hash

from init import db
from models import Assignee, User
from api_requests import get_all_assignees
from json_parsing import get_assignees_fields


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
        'assignee_id': assignees_data[0]["uid"],
        'name': assignees_data[0]["login"],
        'level': 5,
        'rate': 1,
    }
    a = Assignee(**first_assignee_data)
    db.session.add(a)
    db.session.commit()


password = generate_password_hash("123", salt_length=8)


def initialize_users():
    count, assignees_data = get_all_assignees()
    user = assignees_data[0]
    user_data = {
        'login': user["login"],
        'password': password,
        'assignee_id': "8000000000000005"
    }
    u = User(**user_data)
    db.session.add(u)
    db.session.commit()
