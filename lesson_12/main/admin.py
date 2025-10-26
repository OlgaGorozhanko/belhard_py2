from django.contrib import admin

from . import models
# Register your models here.
from .models import Student, Course, Grade

admin.site.register(Student)  #строки 8-10 равносильны этой + прописывают отображение

#@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'sex', 'short_name', 'average_grade2')
    list_display_links = ('surname', 'name')
    # list_editable = ('surname', 'name')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active')

    # для формирования slug
    prepopulated_fields = {"slug": ("name", "surname")}

    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."

    def average_grade(self, obj):
        return '5'

    #     gs = [g.grade for g in obj.grades.all()]
    #     return round(sum(gs)/len(gs),2) if gs else '---'

    def average_grade2(self, obj):
        from django.db.models import Avg
        res = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return res['grade__avg']

    short_name.short_description = "Короткое имя"
    average_grade2.short_description = "Средний бал"
    average_grade.short_description = "Средний бал"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_num", "name", "start_date", "end_date", "description")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("person", "grade", "course", "date")

