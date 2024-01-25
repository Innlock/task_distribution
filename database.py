from werkzeug.security import generate_password_hash

from models import User
from init import db, app
from sqlalchemy import inspect, Column, Integer, String, ForeignKey, Float, Numeric

services_data = [
    "обработка (услуги администрирования)",
    "хранение (услуги администрирования)",
    "дизайн (услуги создания)",
    "развитие (услуги создания)",
    "проектирование (услуги создания)"
]
password = generate_password_hash("123", salt_length=8)
user_data = [["user1", password], ["user2", password]]


def drop_all_tables():
    with app.app_context():
        db.reflect()
        db.drop_all()


# def fill_services():
#     for service_name in services_data:
#         service = Service(name=service_name)
#         db.session.add(service)
#     db.session.commit()


def fill_users():
    for user in user_data:
        u = User(username=user[0], password=user[1])
        db.session.add(u)
    db.session.commit()


drop_all_tables()
fill_user_table = False
with app.app_context():
    # проверить, существует ли таблица и выставить флаг, если нет
    inspector = inspect(db.engine)
    if "user" not in inspector.get_table_names():
        fill_user_table = True

    # создать таблицы
    db.create_all()

    # заполнить таблицы, если они только созданы
    if fill_user_table:
        fill_services()
        fill_users()
