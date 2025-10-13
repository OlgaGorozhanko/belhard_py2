from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Table, Column, func
from datetime import datetime


class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    # будет вписывать дататайм при создании записи
    dateCreate: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False)
    # будет вписывать дататайм при обновлении записи
    dateUpdate: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False)


class UserOrm(Model):
    __tablename__ = 'user'
    name: Mapped[str]
    age: Mapped[int]
    phone: Mapped[str | None]
    # quiz = relationship('QuizOrm', backref='user')


class QuestionOrm(Model):
    __tablename__ = 'question'
    quesion: Mapped[str]
    answer: Mapped[str]
    wrong1: Mapped[str]
    wrong2: Mapped[str]
    wrong3: Mapped[str]


class QuizeOrm(Model):
    __tablename__ = 'quize'
    name_quize: Mapped[str]
    id_quesion1: Mapped[int]
    id_quesion2: Mapped[int]
    id_quesion3: Mapped[int]

