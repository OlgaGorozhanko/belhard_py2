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
    students = Student.objects.prefetch_related('grades__course').all()
    print('-----------------------')
    for s in students:
        c = [f'{g.grade} - {g.course}' for g in s.grades.all()]
        print(s.name, ' - ', c or 'нет оценок')
    for query in connection.queries:
        print(query['sql'])
    print('-----------------------')

    return render(request, 'students.html',
                  context={'students': students})

def student(r, id):
    student = Student.objects.get(id=id)
    return render(r, 'student.html', context={'student': student})


def course(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})
