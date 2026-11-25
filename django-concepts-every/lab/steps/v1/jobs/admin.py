from django.contrib import admin

from .models import Job, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["room", "title", "job", "done"]
    list_filter = ["done"]


admin.site.register(Job)
