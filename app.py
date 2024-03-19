from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import drop_all_tables
from models import *
from init import app, db, login_manager
from distribution import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Роут для главной страницы
@app.route('/')
def index():
    users_list = []
    users = User.query.all()
    for user in users:
        users_list.append({
            'login': user.login,
            'password': user.password
        })

    task_list = []
    tasks = Task.query.all()
    for task in tasks:
        task_list.append({
            'task_id': task.task_id,
            'summary': task.summary,
            'key': task.key,
        })
    distribution = get_tasks_distribution(3)
    res = []
    for assignee, tasks in distribution.items():
        res.append({assignee.name if isinstance(assignee, Assignee) else assignee: [task.key for task in tasks]})
    # res = [users_list, task_list]
    # res = Response(json.dumps(res, ensure_ascii=False).encode('utf-8'), content_type='application/json;charset=utf-8')
    return res


# Роут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка наличия пользователя с таким именем
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким именем уже существует."

        # Создание нового пользователя
        new_user = User(username=username, password=generate_password_hash(password, salt_length=8))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html')


# Роут для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


# Роут для выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/distribution', methods=['GET', 'POST'])
def distribution():
    if request.method == 'POST':
        pass
    distribution_data = get_tasks_distribution(3)
    return render_template('distribution.html', distribution=distribution_data)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=5000)
