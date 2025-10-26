from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Grade, Course
# Create your views here.
from django.db import connection


def index(request):
    return HttpResponse('Hello')
    #return render(request,)

def index2(request):
    context = {
        'login': request.user.username if request.user.is_authenticated else None,
        # другие переменные
    }
    return render(request,'index_1.html', context)

# def students(request):
#     students = Student.objects.all()
#     return render(request, 'students.html', {'students': students})

def students(request):
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

    return render(request, 'students.html',
                  context={'students': students})



def course(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})
