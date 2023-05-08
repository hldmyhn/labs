import requests
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="4laba",
                        user="postgres",
                        password="12345",
                        host="localhost")
cursor = conn.cursor()


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return render_template('login.html', error='Введите логин')
    if not password:
        return render_template('login.html', error='Введите пароль')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if records == []:
        return render_template('account.html')
    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])


@app.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register/', methods=['POST'])
def register_post():
    full_name = request.form.get('full_name')
    username = request.form.get('login')
    password = request.form.get('password')
    if not full_name:
        return render_template('register.html', error='Введите имя')
    if not username:
        return render_template('register.html', error='Введите логин')
    if not password:
        return render_template('register.html', error='Введите пароль')
    cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(username),))
    records = list(cursor.fetchall())
    if records:
        return render_template('register.html', error='Пользователь с таким логином уже существует')
    cursor.execute("INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s)",
                   (str(full_name), str(username), str(password)))
    conn.commit()
    return render_template('account.html', full_name=full_name, login=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)

