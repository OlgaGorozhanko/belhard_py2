from django.contrib import admin

from . import models
# Register your models here.
from .models import Student, Course, Grade

admin.site.register(Student)  #строки 8-10 равносильны этой + прописывают отображение

#@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "sex")
    search_fields = ("surname", "name")

    def average_grade(self, obj):
        return '5'

        # gs = [g.grade for g in obj.grades.all()]
        # return round(sum(gs)/len(gs),2) if gs else '---'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_num", "name", "start_date", "end_date", "description")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("person", "grade", "course", "date")

