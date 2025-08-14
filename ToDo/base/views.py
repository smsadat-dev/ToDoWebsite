from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import TaskModel

# Handles task creatiion, deletion, update and listing 

def processTasks(request):

    if request.method == 'POST':
        TaskTitle = request.POST.get('tasksTitle')
        TaskDesc = request.POST.get('tasksDescrp')
        TaskStatus = request.POST.get('isTaskDone')

        IsDone = True if TaskStatus == 'on' else False

        task = TaskModel(
            taskTitle = TaskTitle,
            taskDescription = TaskDesc,
            isDone =  IsDone
        )
        task.save()

        # redirect to same page to prevent resubmission
        return redirect('base:task')

    if request.method == 'GET':
        tasks = TaskModel.objects.all()
        return render(request, 'taskview.html', {'tasks' : tasks})