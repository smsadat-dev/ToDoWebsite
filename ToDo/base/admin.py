from django.contrib import admin

from .models import TaskModel

# Registered TaskModel to admin panel
admin.site.register(TaskModel)