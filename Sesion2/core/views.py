from django.shortcuts import render

from .models import Task


def home(request):
    return render(request, 'core/home.html')


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'core/task_list.html', {'tasks': tasks})
