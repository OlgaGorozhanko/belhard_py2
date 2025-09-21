from flask import Flask, render_template, redirect, request, url_for, session
import os
from req_api import get_pic_fox, get_pic_duck, get_pic_duck2, get_weather
from clients_DB import check_valid, add_client, is_client


# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места

# app = Flask(__name__)

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

# для сессий обязательно
app.config['SECRET_KEY'] = 'my secret key 12334 dslkfj dlskjf lsdkjf sdlkjflsdkjf'



@app.route("/")
def index():
    login = None
    if session and session['user_id']:
        login = session['user_id']
    return render_template('index.html', login=login)


@app.route("/duck/")
def duck():
    if session and session['user_id']:
        _duck = get_pic_duck2()
        return render_template('duck.html', duck=_duck, login=session['user_id'])
    return redirect(url_for("autorize"))

@app.route("/fox/")
def fox_start():
    if session and session['user_id']:
        _fox = get_pic_fox(1)
        return render_template("fox.html", foxes=_fox, mess="можно только от 1 до 10", login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/fox/<int:num>/")
def fox(num):
    if session and session['user_id']:
        if 1 <= num <= 10:
            _fox = get_pic_fox(num)
            return render_template('fox.html', foxes=_fox, login=session['user_id'])
        return render_template("fox.html", foxes=[], mess="можно только от 1 до 10", login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/weather-minsk/")
def weather_minsk():
    if session and session['user_id']:
        _weather_m = get_weather("Minsk")
        return render_template("weather-minsk.html", weather=_weather_m, login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/weather/")
def weather():
    if session and session['user_id']:
        _weather = get_weather("Minsk")
        return render_template("weather.html", city="Minsk", weather=_weather, login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/weather/<city>/")
def weather_city(city):
    if session and session['user_id']:
        _weather = get_weather(city)
        return render_template("weather.html", city=city, weather=_weather, login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/rainbow/")
def rainbow():
    if session and session['user_id']:
        return render_template("rainbow.html", login=session['user_id'])
    return redirect(url_for("autorize"))


@app.route("/weth/")
def weth():
    if session and session['user_id']:
        return render_template("weth.html")
    return redirect(url_for("autorize"))



@app.route("/register/", methods=["GET", "POST"])
def register():
    render_html = "register.html"
    err = login = None
    if request.method == "POST":
        print(f'{request.form.get("fio")}, {request.form.get("login")}, {request.form.get("password")}, {request.form.get("email")}, {request.form.get("age")}')
        _check_valid = check_valid(request.form.get("fio"), request.form.get("login"), request.form.get("password"), request.form.get("email"), request.form.get("age"))
        login = session['user_id']
        if _check_valid == True:
            add_client(request.form.get("fio"), request.form.get("login"), request.form.get("password"), request.form.get("email"), request.form.get("age"))
            return redirect(url_for("autorize", login=session['user_id']))
        else:
            err = _check_valid
    return render_template(render_html, err=err, login=login)


@app.route("/autorize/", methods=["GET", "POST"])
def autorize():
    """ путь добавляет /autorize/. Почему?

    :return:
    """
    err = None
    render_html = "autorize.html"
    if request.method == "POST":
        if is_client(request.form.get("login"), request.form.get("password")):
            session['user_id'] = request.form.get("login")
            return redirect(url_for("index", login=session['user_id']))
        else:
            err = "Неверный логин/пароль"
    return render_template(render_html, err=err)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)