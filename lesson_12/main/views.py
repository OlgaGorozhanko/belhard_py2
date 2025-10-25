from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Grade, Course


from django.db import connection


def index(request):
    return HttpResponse('Hello')

def index2(request):
    context = {
        'login': request.user.username if request.user.is_authenticated else None,
        # другие переменные
    }
    return render(request,'index_1.html', context)

# def students(request):
#     students = Student.objects.all()
#     return render(request, 'students.html', {'students': students})


def course(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def students(r):
    # взять всех студентов но при это связи на загрузятся
    # они будут грузиться автоматом при запросе для каждого студента отдельно
    # сколько студентов столько запросов
    # students = Student.objects.all()

    # загрузить сразу отдельным запросом курсы из каждого студента
    # 2 запроса при любом количестве данных
    # students = Student.objects.prefetch_related('course').all()

    # или к примеру отдельным запросом по цепочке (двойное подчеркивание)
    # студенты -> у студентов оценки -> у оценок ее курс
    # 3 запроса при любом количестве данных
    students = Student.objects.prefetch_related('grades__course').all()
    # еще более сложная цепочка
    # students = Student.objects.prefetch_related('grades__course__student_set').all()

    for s in students:
        c = [f'{g.grade} - {g.course}' for g in s.grades.all()]
        # print(type(c))
        print(s.name, ' - ', c or 'нет оценок')

    print('-----------------------')
    print(f"Запросов: {len(connection.queries)}")
    for query in connection.queries:
        print(query['sql'])

    return render(r, 'students.html',
                  context={'students': students})


def student(r, id):
    student = Student.objects.get(id=id)
    return render(r, 'student.html', context={'student': student})


# ---------------

# список
class StudentsView(ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'

# просмотр одной записи
class StudentView(DetailView):
    model = Student
    template_name = 'student.html'
   # slug_url_kwarg = 'name_slug'
    context_object_name = 'student'
    # pk_url_kwarg = 'pk' # т.к. тут slug ссылка по id уже не нужна
    # login_url = '/login/'
