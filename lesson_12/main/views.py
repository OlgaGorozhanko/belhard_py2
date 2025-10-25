from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Grade, Course
# Create your views here.

def index(request):
    return HttpResponse('Hello')
    #return render(request,)

def index2(request):
    context = {
        'login': request.user.username if request.user.is_authenticated else None,
        # другие переменные
    }
    return render(request,'index_1.html', context)

def students(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})


def course(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})
