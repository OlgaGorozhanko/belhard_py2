from flask import Flask, render_template
import os
from req_api import get_pic_fox, get_pic_duck, get_pic_duck2, get_weather

# BASE_DIR = os.getcwd()
BASE_DIR = os.path.dirname(__name__) # так работает если проект открыт из любого места

# app = Flask(__name__)

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))


# users = ['user1', 'user22', 'user333', 'suer4', 'user55', 'user6666']


@app.route("/")
def index():
    return render_template('main.html', admin=True, q=22222222)


@app.route("/duck/")
def duck():
    _duck = get_pic_duck2()
    return render_template('duck.html', duck=_duck)

@app.route("/fox/")
def fox_start():
    return render_template("fox.html", foxes=[], mess="можно только от 1 до 10")


@app.route("/fox/<int:num>/")
def fox(num):
    if 1 <= num <= 10:
        _fox = get_pic_fox(num)
        print(_fox, type(_fox))
        return render_template('fox.html', foxes=_fox)
    return render_template("fox.html", foxes=[], mess="можно только от 1 до 10")


@app.route("/weather-minsk/")
def weather_minsk():
    _weather_m = get_weather("Minsk")
    return render_template("weather-minsk.html", weather=_weather_m)


@app.route("/weather/<city>/")
def weather_city(city):
    _weather = get_weather(city)
    return render_template("weather.html", city=city, weather=_weather)


@app.route("/rainbow/")
def rainbow():
    return render_template("rainbow.html")


@app.route("/weth/")
def weth():
    return render_template("weth.html")

# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)