from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from .models import TaskModel

# Handles task creatiion, deletion, update and listing 

def processTasks(request):

    if request.method == 'POST':
        action = request.POST.get('action')
    # ---------------- CREATE TASK ---------------- #
        if action == 'create':

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

            # return JSON model
            return JsonResponse({
                'status' : 'Success',
                'message': 'Task created successfully',
                'task': {
                    #'id': task.id,
                    'taskTitle': task.taskTitle,
                    'taskDescription': task.taskDescription,
                    'creationTime': str(task.creationTime),
                    'isDone': task.isDone,
                }  
            })
        
    # ---------------- UPDATE TASK ---------------- #

        elif action == 'update':    
            task_id = request.POST.get('task_id')
            is_done = request.POST.get('is_done') == 'true'

            try:
                task = TaskModel.objects.get(id=task_id)
                task.isDone = is_done
                task.save()
                return JsonResponse({'status': 'Success', 'message': 'Task updated'})

            except TaskModel.DoesNotExist:
                return JsonResponse({'status': 'Error', 'message': 'Task not found'})

    # ---------------- DELETE TASK ---------------- #

        elif action == 'delete':
            task_id = request.POST.get('task_id')

            try:
                task = TaskModel.objects.get(id=task_id)
                task.delete()
                return JsonResponse({'status': 'Success', 'message': 'Task deleted'})

            except TaskModel.DoesNotExist:
                return JsonResponse({'status': 'Error', 'message': 'Task not found'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    # ---------------- GET TASKS (LIST) ---------------- #
    if request.method == 'GET':
        tasks = TaskModel.objects.all()
        return render(request, 'taskview.html', {'tasks' : tasks})