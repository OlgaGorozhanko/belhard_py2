import os
from random import shuffle

from flask import Flask, render_template, redirect, request, url_for, session
from model import db_add_data, db, Quiz, Question
from req_api import get_weather, get_pic_duck2, get_pic_fox
from clients_DB import is_client, login_check, check_valid, add_client


BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'database')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static/css'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SECRET_KEY'] = 'my secret key 12334 dslkfj dlskjf lsdkjf sdlkjflsdkjf'

db.init_app(app)

html_config = {
    'admin': True,
    'debug': False
}

with app.app_context():
    db_add_data()


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
            return redirect(url_for("index",
                                    login=session.get('user_id')))
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
            return redirect(url_for("autorize",
                                    login=session.get('user_id')))
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
    return render_template('duck.html',
                           duck=_duck,
                           login=session['user_id'])


@app.route("/fox/", endpoint='get_fox_start')
@login_check
def get_fox_start():
    _fox = get_pic_fox(1)
    return render_template("fox.html",
                           foxes=_fox,
                           mess="можно только от 1 до 10",
                           login=session['user_id'])


@app.route("/fox/<int:num>/", endpoint='get_fox')
@login_check
def get_fox(num):
    if 1 <= num <= 10:
        _fox = get_pic_fox(num)
        return render_template('fox.html',
                               foxes=_fox,
                               login=session.get("user_id"))
    return render_template("fox.html",
                           foxes=[],
                           mess="можно только от 1 до 10",
                           login=session.get("user_id"))


@app.route("/weather-minsk/", endpoint="get_weather_minsk")
@login_check
def get_weather_minsk():
    _weather_m = get_weather("Minsk")
    return render_template("weather-minsk.html",
                           weather=_weather_m,
                           login=session.get("user_id"))


@app.route("/weather/", endpoint="weather")
@login_check
def weather():
    _weather = get_weather("Minsk")
    return render_template("weather.html",
                           city="Minsk",
                           weather=_weather,
                           login=session.get("user_id"))


@app.route("/weather/<city>/", endpoint="get_weather_city")
@login_check
def get_weather_city(city):
    _weather = get_weather(city)
    return render_template("weather.html",
                           city=city,
                           weather=_weather,
                           login=session.get("user_id"))


@app.route("/rainbow/", endpoint="get_rainbow")
@login_check
def get_rainbow():
    return render_template("rainbow.html",
                           login=session.get("user_id"))


@app.route('/tags/', endpoint="get_task_5")
@login_check
def get_task_5():
    return render_template("tags.html",
                           login=session.get("user_id"))


@app.route('/quiz/', endpoint="quiz", methods=["GET", "POST"])
@login_check
def quiz():
    print("quiz()")
    #return render_template("quiz.html", login=session.get("user_id"))
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        print(f"quizes -- {quizes}")
        return render_template('quiz.html',
                               quizes=quizes,
                               html_config=html_config,
                               login=session.get("user_id"))
    print("quiz() request.method == 'POST'")
    session.update({
        'quiz_id': request.form.get('quiz'),
        'question_n': 0,
        'question_id': 0,
        'right_answers': 0
    })
    return redirect(url_for('view_question'))


@app.route('/question/', methods=['POST', 'GET'])
def view_question():
    print("view_question()")
    print(f"session.get('quiz_id') --{session.get('quiz_id')}, session.get('quiz_id') -{session.get('quiz_id')}" )
    if not session.get('quiz_id') or session.get('quiz_id') == -1:
        return redirect(url_for('quiz'))
    # если пост значит ответ на вопрос
    if request.method == 'POST':
        question = Question.query.filter_by(id=session.get('question_id')).all()[0]
        # если ответы сходятся значит +1
        if question.answer == request.form.get('ans_text'):
            session['right_answers'] += 1
        # следующий вопрос
        session['question_n'] += 1
    quiz = Quiz.query.filter_by(id=session.get('quiz_id')).all()
    if int(session.get('question_n')) >= len(quiz[0].question):
        session['quiz_id'] = -1  # чтобы больше не работала страница question
        return redirect(url_for('view_result'))
    else:
        question = quiz[0].question[session.get('question_n')]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3]
        shuffle(answers)  # shuffle -- перемешать
        return render_template('question.html',
                               answers=answers,
                               question=question,
                               html_config=html_config,
                               login=session.get("user_id"))


@app.route('/result/')
def view_result():
    return render_template('result.html',
                    right=session.get('right_answers'),
                    total=session.get('question_n'),
                    html_config=html_config,
                    login=session.get("user_id"))


@app.route('/quiz/editor/', methods=['POST', 'GET'])
def view_quiz_edit():
    if request.method == 'POST':
        quiz = request.form.get('quiz')
        if quiz and len(quiz) > 3:
            quiz = Quiz(quiz)
            db.session.add(quiz)
            db.session.commit()
        else:
            fields = ['question', 'answer', 'wrong1', 'wrong2', 'wrong3']
            question, answer, wrong1, wrong2, wrong3 = [request.form.get(f) for f in fields]
            if all([question, answer, wrong1, wrong2, wrong3]):
                q = Question(question, answer, wrong1, wrong2, wrong3)
                db.session.add(q)
                db.session.commit()
        return redirect(url_for('view_quiz_edit',
                                qqq='123',
                                login=session.get("user_id")))
    # если GET
    quizes = Quiz.query.all()
    questions = Question.query.all()
    return render_template('quizes_editor.html',
                           html_config=html_config,
                           quizes=quizes,
                           questions=questions,
                           len=len,
                           login=session.get("user_id"))


# Сработает если ошибка 404 - т.е. любой другой путь который выше не предусмотрен
@app.errorhandler(404)
def page_not_found(error):
    return '<h1 style="color:red">такой страницы не существует</h1>'


app.run(debug=True)
