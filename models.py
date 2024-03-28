from flask import json

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

    def __repr__(self):
        return f'<Пользователь {self.login}>'

    def get_id(self):
        return self.user_id

    def get_login(self):
        return self.login


# Исполнители
class Assignee(db.Model):
    __tablename__ = 'assignees'
    assignee_id = Column(String(16), primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)
    level = Column(Integer, default=1)  # Насколько сложные и срочные задачи решает (1-5)
    rate = Column(Numeric, default=1.0)  # Ставка [1, 0.5]
    tasks = relationship('Task', back_populates='assignee')

    def __repr__(self):
        return f'<Исполнитель. Логин: {self.name}, уровень: {self.level}, ставка: {self.rate}>'


# Очереди
class Queue(db.Model):
    __tablename__ = 'queues'
    queue_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)

    def __repr__(self):
        return f'<Очередь. Название: {self.name}'


# Задачи
class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = Column(String(24), primary_key=True)  # ID задачи в трекере
    summary = Column(String(50), nullable=False)  # Название задачи в трекере
    key = Column(String(50), nullable=False)  # Ключ задачи в трекере (для обращения к задаче  позже)
    status = Column(String(50), nullable=False)  # Статус задачи (open/inProgress/needInfo)
    priority = Column(Integer, default=3)  # Приоритетность задачи (1-5)
    complexity = Column(Integer, default=3)  # Сложность задачи (1-5)
    estimation = Column(String(50))  # Оценка времени задачи (ISO 8601 duration string) в реальном времени
    # time_spent = Column(String(50))  # Потраченное на задачу время (ISO 8601 duration string) в реальном времени
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'))
    assignee = relationship('Assignee', back_populates='tasks')

    def __repr__(self):
        return (f'<Задача. Название: {self.summary}, '
                f'приоритет: {self.priority}, сложность: {self.complexity}, оценка времени: {self.estimation}>')


# Спринты
class Sprint(db.Model):
    __tablename__ = 'sprints'
    sprint_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)

    def __repr__(self):
        return f'<Спринт. Название: {self.name}, начало спринта: {self.startDate}, конец спринта: {self.endDate}'


# Сфера задачи/сотрудника (например, бекенд/фронтенд)
class Component(db.Model):
    __tablename__ = 'components'
    component_id = Column(Integer, primary_key=True)  # ID в трекере
    name = Column(String(250), nullable=False)

    def __repr__(self):
        return f'<Компонент. Название: {self.name}'


# Таблицы связей мн к мн
class AssigneesQueues(db.Model):
    __tablename__ = "assignees_queues"
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'), primary_key=True)
    queue_id = Column(Integer, ForeignKey('queues.queue_id'), primary_key=True)


class TasksQueues(db.Model):
    __tablename__ = "tasks_queues"
    task_id = Column(String(24), ForeignKey('tasks.task_id'), primary_key=True)
    queue_id = Column(Integer, ForeignKey('queues.queue_id'), primary_key=True)


class TasksSprints(db.Model):
    __tablename__ = "tasks_sprints"
    task_id = Column(String(24), ForeignKey('tasks.task_id'), primary_key=True)
    sprint_id = Column(Integer, ForeignKey('sprints.sprint_id'), primary_key=True)


class TasksComponents(db.Model):
    __tablename__ = "tasks_components"
    task_id = Column(String(24), ForeignKey('tasks.task_id'), primary_key=True)
    component_id = Column(Integer, ForeignKey('components.component_id'), primary_key=True)


class AssigneesComponents(db.Model):
    __tablename__ = "assignees_components"
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'), primary_key=True)
    component_id = Column(Integer, ForeignKey('components.component_id'), primary_key=True)


# Таблицы на время работы пользователя с приложением

# План/черновик распределения задач между сотрудниками
class Assignment(db.Model):
    __tablename__ = 'assignment_temp'
    assignment_id = db.Column(db.Integer, primary_key=True)  # Номер распределения на случай если их будет много
    name = db.Column(db.String(250), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    queue_id = db.Column(db.Integer, db.ForeignKey('queues.queue_id'), nullable=False)
    sprint_id = db.Column(db.Integer, db.ForeignKey('sprints'))


# Распределение задач между сотрудниками
class AssigneesTasksTemp(db.Model):
    __tablename__ = "assignee_task_temp"
    task_id = Column(String(24), ForeignKey('tasks.task_id'), primary_key=True)
    assignee_id = Column(String(16), ForeignKey('assignees.assignee_id'), primary_key=True)
    assignment_id = Column(Integer, ForeignKey('assignment_temp.assignment_id'), primary_key=True)
