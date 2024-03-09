from init import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Numeric, DateTime, Table
from sqlalchemy.orm import relationship


# Пользователи приложения
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    login = Column(String(80), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'))


# Исполнители
class Assignee(db.Model):
    __tablename__ = 'assignees'
    assignee_id = Column(String(16), primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)
    level = Column(Integer, default=1)  # Насколько сложные и срочные задачи решает (1-5)
    rate = Column(Numeric, default=1.0)  # Ставка [1, 0.5]
    tasks = relationship('Task', back_populates='assignee')


# Очереди
class Queue(db.Model):
    __tablename__ = 'queues'
    queue_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)


# Задачи
class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = Column(String(24), primary_key=True)  # ID задачи в трекере
    summary = Column(String(50), nullable=False)  # Название задачи в трекере
    key = Column(String(50), nullable=False)  # Ключ задачи в трекере (для обращения к задаче  позже)
    priority = Column(Integer, default=1)  # Приоритетность задачи (1-5)
    complexity = Column(Integer, default=1)  # Сложность задачи (1-5)
    status = Column(String(50), nullable=False)  # Статус задачи (open/inProgress/needInfo)
    estimation = Column(String(50))  # Оценка времени задачи (ISO 8601 duration string) в реальном времени
    time_spent = Column(String(50))  # Потраченное на задачу время (ISO 8601 duration string) в реальном времени
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'))
    assignee = relationship('Assignee', back_populates='tasks')


# Спринты
class Sprint(db.Model):
    __tablename__ = 'sprints'
    sprint_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)


# Сфера задачи/сотрудника (например, бекенд/фронтенд)
class Component(db.Model):
    __tablename__ = 'components'
    component_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)


# Таблицы связей мн к мн
assignee_queue = db.Table('assignee_queue',
                          db.Column('assignee_id', String(16), ForeignKey('assignees.assignee_id')),
                          db.Column('queue_id', Integer, ForeignKey('queues.queue_id'))
                          )

task_queue = db.Table('task_queue',
                      db.Column('task_id', String(24), ForeignKey('tasks.task_id')),
                      db.Column('queue_id', Integer, ForeignKey('queues.queue_id'))
                      )

task_sprint = db.Table('task_sprint',
                       db.Column('task_id', String(24), ForeignKey('tasks.task_id')),
                       db.Column('sprint_id', Integer, ForeignKey('sprints.sprint_id'))
                       )

task_component = db.Table('task_component',
                          db.Column('task_id', String(24), ForeignKey('tasks.task_id')),
                          db.Column('component_id', Integer, ForeignKey('components.component_id'))
                          )

assignee_component = db.Table('assignee_component',
                              db.Column('assignee_id', String(16), ForeignKey('assignees.assignee_id')),
                              db.Column('component_id', Integer, ForeignKey('components.component_id'))
                              )


# Таблицы на время работы пользователя с приложением

# План/черновик распределения задач между сотрудниками
class Assignment(db.Model):
    __tablename__ = 'assignment_temp'
    assignment_id = db.Column(db.Integer, primary_key=True)  # Номер распределения на случай если их будет много
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    queue_id = db.Column(db.Integer, db.ForeignKey('queues.queue_id'))
    name = db.Column(db.String(250))


# Распределение задач между сотрудниками
assignee_task_temp = db.Table('assignee_task_temp',
                              db.Column('task_id', String(24), ForeignKey('tasks.task_id')),
                              db.Column('assignee_id', String(16), ForeignKey('assignees.assignee_id')),
                              db.Column('assignment_id', Integer, ForeignKey('assignment_temp.assignment_id'))
                              )
