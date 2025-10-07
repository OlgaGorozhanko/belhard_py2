import random

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     # __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String(25))
#
#     quizes = db.relationship('Quiz', backref='user',
#                              cascade = "all, delete, delete-orphan",
#                              lazy='select')
#         # lazy -
#             # select (по умолчанию)   Загружает всю коллекцию одним отдельным SELECT-запросом при первом обращении к атрибуту
#             # joined  Загружает коллекцию сразу через JOIN с основной таблицей
#             # subquery    Загружает коллекцию через подзапрос
#             # dynamic Возвращает query-объект, коллекция не загружается сразу, можно строить запросы
#
#     def __init__(self, name) -> None:
#         super().__init__()
#         self.name = name


quiz_question = db.Table('quiz_question',
                         db.Column('quiz_id', db.Integer, db.ForeignKey('quiz.id'), primary_key=True),
                         db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
                         )


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    # пишем только в одной из 2х таблиц - во второй появиться автоматом
    # question = db.relationship(
    #             'Question',
    #             secondary=quiz_question, backref = 'quiz')

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return f'id - {self.id}, name - {self.name}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    wrong1 = db.Column(db.String(100), nullable=False)
    wrong2 = db.Column(db.String(100), nullable=False)
    wrong3 = db.Column(db.String(100), nullable=False)

    quiz = db.relationship(
        'Quiz',
        secondary=quiz_question, backref='question')

    def __init__(self, quesion: str, answer, wrong1, wrong2, wrong3) -> None:
        super().__init__()
        self.question = quesion
        self.answer = answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    def __repr__(self):
        return f'{self.id}-{self.question}'


def db_add_data():
    db.drop_all()
    db.create_all()

    quizes = [
        Quiz('Квиз 1'),
        Quiz('Квиз 2'),
        Quiz('Квиз 3'),
        Quiz('Квиз 4')
    ]

    questions = [
        Question('Сколько будут 2+2*2', '6', '8', '2', '0'),
        Question('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
        Question('Каким станет зелёный утёс, если упадет в Красное море?', 'Мокрым?', 'Красным', 'Не изменится',
                 'Фиолетовым'),
        Question('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        Question('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море',
                 'Воздух'),
        Question('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы',
                 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        Question('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако'),
        Question('Что такое у меня в кармашке?', 'Кольцо', 'Кулак', 'Дырка', 'Бублик')
    ]

    for _quize in quizes:
        used_questions = []
        for _ in range(random.randint(3, 6)):  # рандомно от 3 до 6 вопросов в квизе
            while True:
                rand_num = random.randint(0, len(questions) - 1) # рандомные вопросы из всех
                if rand_num not in used_questions:
                    _quize.question.append(questions[rand_num])
                    used_questions.append(rand_num)
                    break

    # сохраняем всё в БД
    db.session.add_all(quizes)
    db.session.commit()
