import json
from typing import Union

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed

from .models import TaskModel

# Handles task creatiion, deletion, update and listing 

def processTasks(request) -> Union[HttpResponse, JsonResponse]:

    # ---------------- CREATE TASK ---------------- #
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

        # return JSON model
        return JsonResponse({
            'status' : 'success',
            'message': 'Task created successfully',
            'task': {
                # 'id': task.id,
                'taskTitle': task.taskTitle,
                'taskDescription': task.taskDescription,
                'creationTime': str(task.creationTime),
                'isDone': task.isDone,
            }  
        })
        
    # ---------------- UPDATE TASK ---------------- #

    elif request.method in ['PUT', 'PATCH']:
        
        try: 
            data = json.loads(request.body.decode('utf-8'))
            task_id = data.get('task_id')
            is_done = data.get('is_done', False) # default False if not sent

        except(json.JSONDecodeError, AttributeError): 
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        try:
            task = TaskModel.objects.get(id=task_id)
            task.isDone = is_done
            task.save()
            return JsonResponse({'status': 'success', 'message': 'Task updated'})

        except TaskModel.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': 'Task not found'})

    # ---------------- DELETE TASK ---------------- #

    elif request.method == 'DELETE':
        
        try: 
            data = json.loads(request.body.decode('utf-8'))
            task_id = data.get('task_id')
        except(json.JSONDecodeError, AttributeError): 
            return JsonResponse({'status': 'error', 'message':'Invalid request'}, status=400)

        try:
            task = TaskModel.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'status': 'success', 'message': 'Task deleted'})

        except TaskModel.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': 'Task not found'}, status=404)

    # ---------------- GET TASKS (LIST) ---------------- #

    elif request.method == 'GET':
        tasks = TaskModel.objects.all()
        return render(request, 'taskview.html', {'tasks' : tasks})
    
    else:
        # any other HTTP method
        return HttpResponseNotAllowed(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])


    