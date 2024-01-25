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
    assignee_id = relationship('Assignee', back_populates="user", uselist=False)  # lazy='dynamic'


# Исполнители
class Assignee(db.Model):
    __tablename__ = 'assignees'
    assignee_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    level = Column(Integer, default=1)  # Насколько сложные задачи решает
    rate = Column(Numeric, default=1.0)  # Ставка
    user_id = relationship('User', back_populates="assignee")


# Очереди
class Queue(db.Model):
    __tablename__ = 'queues'
    queue_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# Задачи
class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    priority = Column(Integer, default=1)  # Приоритетность задачи
    estimation = Column(Integer, default=1)  # Сложность задачи
    assignee_id = relationship('Assignee', back_populates="task", uselist=False)


# Спринты
class Sprint(db.Model):
    __tablename__ = 'sprints'
    sprint_id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)  # Дата спринта (для сопоставления с датами задач) -- Мб сделать номер??


# Тэги (для классификации задач)
class Tag(db.Model):
    __tablename__ = 'tags'
    tag_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# Сфера задачи/сотрудника (например, бекенд/фронтенд)
class Component(db.Model):
    __tablename__ = 'components'
    component_id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# Таблицы связей мн к мн
assignee_queue = Table('assignee_queue',
                       db.Column('assignee_id', Integer, ForeignKey('assignees.assignee_id')),
                       db.Column('queue_id', Integer, ForeignKey('queues.queue_id'))
                       )

queue_task = Table('queue_task',
                   db.Column('task_id', Integer, ForeignKey('tasks.task_id')),
                   db.Column('queue_id', Integer, ForeignKey('queues.queue_id'))
                   )

task_sprint = Table('task_sprint',
                    db.Column('task_id', Integer, ForeignKey('tasks.task_id')),
                    db.Column('sprint_id', Integer, ForeignKey('sprints.sprint_id'))
                    )

task_tag = Table('task_tag',
                 db.Column('task_id', Integer, ForeignKey('tasks.task_id')),
                 db.Column('tag_id', Integer, ForeignKey('tags.tag_id'))
                 )

task_component = Table('task_component',
                       db.Column('task_id', Integer, ForeignKey('tasks.task_id')),
                       db.Column('component_id', Integer, ForeignKey('components.component_id'))
                       )

assignee_component = Table('assignee_component',
                           db.Column('assignee_id', Integer, ForeignKey('assignees.assignee_id')),
                           db.Column('component_id', Integer, ForeignKey('components.component_id'))
                           )


# Таблицы на время работы пользователя с приложением

# План/черновик распределения задач между сотрудниками
class Assignment(db.Model):
    __tablename__ = 'assignment_temp'
    assignment_id = db.Column(db.Integer, primary_key=True)  # Номер распределения на случай если их будет много
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    queue_id = db.Column(db.Integer, db.ForeignKey('queues.queue_id'))


# Распределение задач между сотрудниками
class TaskAssignee(db.Model):
    __tablename__ = 'assignee_task_temp'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignees.assignee_id'))
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment_temp.assignment_id'))
