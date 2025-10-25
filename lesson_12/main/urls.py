from django.urls import path, include, re_path

from .views import *

urlpatterns = [
    # через функции и id
    path('students/', students, name='students'),
    path('students/<int:id>/', student, name='student'),

    # через класс и slug
    path('students2/', StudentsView.as_view(), name='students2'),
    path('students2/<slug:name_slug>/', StudentView.as_view(), name='student2'),



]