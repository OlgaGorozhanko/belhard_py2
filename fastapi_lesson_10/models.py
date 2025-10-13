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



class QuestionOrm(Model):
    __tablename__ = 'question'
    question: Mapped[str]
    answer: Mapped[str]
    wrong1: Mapped[str]
    wrong2: Mapped[str]
    wrong3: Mapped[str]



class QuizeOrm(Model):
    __tablename__ = 'quize'
    name_quize: Mapped[str]
    id_question1: Mapped[int] = mapped_column(ForeignKey('question.id'), nullable=False)
    id_question2: Mapped[int] = mapped_column(ForeignKey('question.id'), nullable=False)
    id_question3: Mapped[int] = mapped_column(ForeignKey('question.id'), nullable=False)

    question1: Mapped[QuestionOrm] = relationship('QuestionOrm', foreign_keys=[id_question1])
    question2: Mapped[QuestionOrm] = relationship('QuestionOrm', foreign_keys=[id_question2])
    question3: Mapped[QuestionOrm] = relationship('QuestionOrm', foreign_keys=[id_question3])

