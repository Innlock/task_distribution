import time

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


def get_current_id():
    if current_user.is_authenticated:
        user_id = current_user.user_id
        return user_id
    return None


# Роут для главной страницы
@app.route('/')
def index():
    return redirect('/login')
    # distribution = get_tasks_distribution(3)
    # res = []
    # for assignee, tasks in distribution.items():
    #     res.append({assignee.name if isinstance(assignee, Assignee) else assignee: [task.key for task in tasks]})
    #
    # # users_list = []
    # # users = User.query.all()
    # # for user in users:
    # #     users_list.append({
    # #         'login': user.login,
    # #         'password': user.password
    # #     })
    # # task_list = []
    # # tasks = Task.query.all()
    # # for task in tasks:
    # #     task_list.append({
    # #         'task_id': task.task_id,
    # #         'summary': task.summary,
    # #         'key': task.key,
    # #     })
    # # res = [users_list, task_list]
    # # res = Response(json.dumps(res, ensure_ascii=False).encode('utf-8'), content_type='application/json;charset=utf-8')
    # return res
    # # distribution_data = get_tasks_distribution(3)
    # # return render_template('distribution.html', distribution=distribution_data, queue="3", sprint="spr")


# Роут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Проверка наличия пользователя с таким именем
        existing_user = User.query.filter_by(login=username).first()
        if existing_user:
            return render_template('register.html',
                                   error="Пользователь с таким логином уже существует")
        if not login_in_assignees(username):
            return render_template('register.html',
                                   error="Логин не зарегистрирован в организации")

        # Создание нового пользователя
        new_user = User(login=username, password=generate_password_hash(password, salt_length=8))
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('register.html')


# Роут для входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sync_data_in_database()
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(login=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('settings'))
        return render_template('login.html', error="Неверный логин или пароль")
    return render_template('login.html')


# Роут для выхода
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/distribution', methods=['GET', 'POST'])
@login_required
def distribution():
    if request.method == 'POST':
        pass
    queue_text = request.form.get('queue')
    sprint_text = request.form.get('sprint')

    queue_id, queue_name = queue_text.split("_")
    queue_id = int(queue_id)
    print(queue_id, queue_name)

    sprint_id, sprint_name = None, ""
    if sprint_text:
        sprint_id, sprint_name = sprint_text.split("_")

    distribution_data = get_tasks_distribution(queue_id, sprint_id)
    return render_template('distribution.html', distribution=distribution_data,
                           queue=queue_name, sprint=sprint_name)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    queues = get_all_queues()
    sprints = get_all_sprints()
    return render_template('settings.html', login=current_user.login, queues=queues, sprints=sprints)


@app.route('/sync_data', methods=['GET', 'POST'])
@login_required
def sync_data():
    success = False
    res = {}
    try:
        sync_data_in_database(False, current_user.assignee_id)
        success = True
    except Exception as e:
        res = {'error': str(e)}

    if success:
        queues = get_all_queues()
        sprints = get_all_sprints()

        queues = [{"queue_id": queue.queue_id, "name": queue.name} for queue in queues]
        sprints = [{"sprint_id": sprint.sprint_id, "name": sprint.name} for sprint in sprints]
        res = {'success': success, 'queues': queues, 'sprints': sprints}

    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=5000)
