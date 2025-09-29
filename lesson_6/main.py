from flask import Flask, render_template, redirect, request, url_for, session
import os

from req_api import get_weather, get_pic_duck2, get_pic_fox
from clients_DB import is_client, login_check, check_valid, add_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key 12334 dslkfj dlskjf lsdkjf sdlkjflsdkjf'


users = ['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666', 'user77']
user = {'fname': 'Helga', 'lname': 'Gorozhanko'}



# session['num'] = 0 #  так нельзя - можно только внутри ендпоинта (вью-функции)

@app.route("/")
def index():
    login = None
    # session['user_id'] = "Хельга"
    if session.get('user_id'):
        login = session.get('user_id')
    return render_template('index.html', login=login)

@app.route("/autorize/", methods=["GET", "POST"])
def autorize():
    err = None
    render_html = "autorize_1.html"
    if request.method == "POST":
        if is_client(request.form.get("login"), request.form.get("password")):
            session['user_id'] = request.form.get("login")
            return redirect(url_for("index", login=session.get('user_id')))
        else:
            err = "Неверный логин/пароль"
    return render_template(render_html, err=err)


@app.route("/register/", methods=["GET", "POST"])
def register():
    render_html = "register.html"
    err = None
    login = session.get('user_id')
    # err = login = None
    if request.method == "POST":
        print(f'{request.form.get("fio")}, {request.form.get("login")}, {request.form.get("password")}, {request.form.get("email")}, {request.form.get("age")}')
        _check_valid = check_valid(request.form.get("fio"), request.form.get("login"), request.form.get("password"), request.form.get("email"), request.form.get("age"))
        login = session.get('user_id')
        if _check_valid == True:
            add_client(request.form.get("fio"), request.form.get("login"), request.form.get("password"), request.form.get("email"), request.form.get("age"))
            return redirect(url_for("autorize", login=session.get('user_id')))
        else:
            err = _check_valid
    return render_template(render_html, err=err, login=login)


@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route("/duck/")
@login_check
def duck():
    _duck = get_pic_duck2()
    return render_template('duck.html', duck=_duck, login=session['user_id'])


@app.route("/fox/", endpoint='get_fox_start')
@login_check
def get_fox_start():
    _fox = get_pic_fox(1)
    return render_template("fox.html", foxes=_fox, mess="можно только от 1 до 10", login=session['user_id'])


@app.route("/fox/<int:num>/", endpoint='get_fox')
@login_check
def get_fox(num):
    if 1 <= num <= 10:
        _fox = get_pic_fox(num)
        return render_template('fox.html', foxes=_fox, login=session['user_id'])
    return render_template("fox.html", foxes=[], mess="можно только от 1 до 10", login=session['user_id'])


@app.route("/weather-minsk/", endpoint="get_weather_minsk")
@login_check
def get_weather_minsk():
    _weather_m = get_weather("Minsk")
    return render_template("weather-minsk.html", weather=_weather_m, login=session['user_id'])


@app.route("/weather/", endpoint="weather")
@login_check
def weather():
    _weather = get_weather("Minsk")
    return render_template("weather.html", city="Minsk", weather=_weather, login=session['user_id'])


@app.route("/weather/<city>/", endpoint="get_weather_city")
@login_check
def get_weather_city(city):
    _weather = get_weather(city)
    return render_template("weather.html", city=city, weather=_weather, login=session['user_id'])


@app.route("/rainbow/", endpoint="get_rainbow")
@login_check
def get_rainbow():
    return render_template("rainbow.html", login=session["user_id"])


@app.route('/tags/', endpoint="get_task_5")
@login_check
def get_task_5():
    return render_template("tags.html", login=session["user_id"])



# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)
