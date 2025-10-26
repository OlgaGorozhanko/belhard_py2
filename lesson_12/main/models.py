from django.db import models
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator

# Create your models here.


class Student(models.Model):
    name = models.CharField(
        verbose_name='Имя'
        , null=False
        , blank=False
        , help_text='Введите имя'
    )
    surname = models.CharField(
        verbose_name='Фамилия'
        , null=False
        , blank=False
        , help_text='Введите фамилию'
    )
    age = models.SmallIntegerField(
        verbose_name='Возраст'
        , null=True
        , blank=True
        , help_text='Введите возраст'
        , validators=[MinValueValidator(16), MaxValueValidator(100)]
    )

    sex = models.CharField(
        choices=[("f", "Женщина"), ("m", "Мужчина")]
        , verbose_name='Пол'
    )

    active = models.BooleanField(verbose_name="Обучается")

    course = models.ManyToManyField(
        to="Course"
        , blank=True
        , verbose_name="Посещаемые курсы"
    )

    photo = models.ImageField(
        upload_to=r'phontos/%Y/%m/%d/',
        blank=True,
        verbose_name="Фото"
    )

    def __str__(self):
        return f"{self.name} {self.surname} {self.age} {self.sex} {'+' if self.active else '-'}"

    class Meta:  # ??
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        # indexes = [admin.Index(fields=['surname'])]
        ordering = ["surname"]


class Course(models.Model):
    langs = [
        ("py", "Python")
        , ("c#", "C#")
        , ("js", "JavaScript")
    ]

    name = models.CharField(choices=langs, verbose_name="Язык программирования")
    course_num = models.SmallIntegerField(
        default=1
        , verbose_name="Номер курса"
        , validators=[MinValueValidator(1), MaxValueValidator(1000)])
    start_date = models.DateField(verbose_name="Начало курса")
    end_date = models.DateField(verbose_name="Окончание курса")
    description = models.TextField(blank=True
                                   , verbose_name="Описание курса")


    def __str__(self):
        return f"{self.get_name_display()} - {self.course_num}"


class Grade(models.Model):
    person = models.ForeignKey(
        Student
        , on_delete=models.CASCADE
        , related_name="grades"
        , verbose_name="Оценка студента"
    )

    grade = models.PositiveSmallIntegerField(
        default=0
        , validators=[MinValueValidator(1), MaxValueValidator(10)]
        , verbose_name="Оценка"
    )

    course = models.ForeignKey(
            Course
            , null=True
            , on_delete=models.CASCADE
            , verbose_name="КУрс"
        )

    date = models.DateField(
        verbose_name="Дата получения"
        , null=True
    )

