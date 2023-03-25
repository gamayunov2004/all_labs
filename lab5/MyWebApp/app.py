from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="0000",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('username')
            password = request.form.get('password')
            cursor.execute(f"SELECT * FROM service.users WHERE login='{str(login)}' AND password='{str(password)}';")
            records = list(cursor.fetchall())

            if not login or not password:
                return render_template("login.html", message="Введите логин и пароль!")
            if len(records) == 0:
                return render_template("login.html", message="Неверное имя пользователя или пароль!")
            else:
                return render_template('account.html', full_name=records[0][1], login=login, password=password)
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute(f"SELECT * FROM service.users WHERE login='{str(login)}'")
        bd = list(cursor.fetchall())
        if login and password and name and len(bd)==0:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);'
                           , (str(name), str(login), str(password)))
            conn.commit()
        if not login or not password or not name:
            return render_template("registration.html", message="Введите данные!")
        if len(bd)>0:
            return render_template("registration.html", message="Пользователь уже существует!")

        return redirect('/login/')
    return render_template('registration.html')