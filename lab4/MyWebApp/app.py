from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="0000",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())

    if not username or not password:
        return render_template("login.html", message="Введите логин и пароль!")
    if len(records)==0:
        return render_template("login.html", message="Неверное имя пользователя или пароль!")
    else:
        return render_template('account.html', full_name=records[0][1], login=username, password=password)