from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Scheduler)
admin.site.register(Job)
admin.site.register(Task)
admin.site.register(TaskDependency)
admin.site.register(TaskDefinition)
admin.site.register(Log)
