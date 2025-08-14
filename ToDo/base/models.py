from django.db import models

# Task model

class TaskModel(models.Model):

    taskTitle = models.CharField(null=False, max_length=200, unique=False)
    taskDescription = models.TextField()
    creationTime = models.TimeField(auto_now_add=True)
    isDone = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.taskTitle

    class Meta:
        ordering = ['-creationTime']
